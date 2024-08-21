import instaloader
from instaloader import Profile
from django.db import models
from django.utils import timezone
import re

import pytz
import logging

from utils.comparators.media_comparator import MediaComparator

from ...models.post import FetchedPost

logging.basicConfig(filename='fetched_posts.log', level=logging.INFO)


class InstagramPublishChecker:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        self.media_comparator = MediaComparator()

    def check_post(self, schedule):
        try:
            # Instagram profilini yükle
            instagram_profile = schedule.post.user.user_profile.instagram_username
            profile = Profile.from_username(self.loader.context, instagram_profile)

            fetched_posts = []
            scheduled_date_utc = schedule.scheduled_date.astimezone(pytz.utc)

            for post in profile.get_posts():
                post_date_utc = post.date_utc.replace(tzinfo=pytz.utc) 
                if post_date_utc <= scheduled_date_utc:
                    fetched_posts.append(post)
                if post_date_utc < scheduled_date_utc - timezone.timedelta(days=1): 
                    break

            for fetched_post in fetched_posts:
                if self.compare_post(fetched_post, schedule):
                    schedule.published_date = fetched_post.date_utc 
                    schedule.status = 'published'
                    schedule.save()

                    FetchedPost.objects.create(
                        schedule=schedule,
                        post_id=fetched_post.shortcode,
                        caption=fetched_post.caption,
                        media_urls=[media.video_url if media.is_video else media.display_url for media in fetched_post.get_sidecar_nodes()] if fetched_post.typename == "GraphSidecar" else [fetched_post.video_url if fetched_post.is_video else fetched_post.url]
                    )

                    logging.info(f"Fetched Post: {fetched_post.shortcode}, Caption: {fetched_post.caption}, Media URLs: {[media.video_url if media.is_video else media.display_url for media in fetched_post.get_sidecar_nodes()] if fetched_post.typename == "GraphSidecar" else [fetched_post.video_url if fetched_post.is_video else fetched_post.url]}")

                    break  # Eşleşme bulunduğunda döngüden çık

        except instaloader.exceptions.ProfileNotExistsException:
            # Profil bulunamadıysa
            schedule.status = 'failed'
            schedule.save()
            logging.error(f"Profil bulunamadı: {instagram_profile}")

        except instaloader.exceptions.LoginRequiredException:
            # Oturum açma gerekiyorsa
            schedule.status = 'failed'
            schedule.save()
            logging.error("Instagram oturum açma gerekiyor.")

        except Exception as e:
            # Diğer beklenmeyen hatalar
            schedule.status = 'failed'
            schedule.save()
            logging.error(f"Beklenmeyen hata: {e}")

    def compare_post(self, fetched_post, schedule):
        try:
            if self.normalize_caption(fetched_post.caption) != self.normalize_caption(schedule.post.content):
                return False

            scheduled_media = schedule.post.medias.all()
            fetched_media_urls = self.get_all_fetched_media_urls(fetched_post)

            if len(scheduled_media) != len(fetched_media_urls):  # Check if media counts match
                return False

            for i in range(len(scheduled_media)):
                media = scheduled_media[i]
                fetched_media_url = fetched_media_urls[i]

                if media.media_type == 'image':
                    comparison_result = self.media_comparator.compare_images(media.file.path, fetched_media_url)
                elif media.media_type == 'video':
                    comparison_result = self.media_comparator.compare_videos(media.file.path, fetched_media_url)

                if not comparison_result['is_similar']:
                    return False

            return True

        except Exception as e:
            logging.error(f"Medya karşılaştırma hatası: {e}")
            return False  # Karşılaştırma sırasında hata oluşursa False döndür

    def get_all_fetched_media_urls(self, fetched_post):
        if fetched_post.typename == "GraphSidecar":
            return [node.video_url if node.is_video else node.display_url for node in fetched_post.get_sidecar_nodes()]
        else:
            return [fetched_post.video_url if fetched_post.is_video else fetched_post.url]
        
    def normalize_caption(self, caption):
        if caption:
            # Satır sonu karakterlerini kaldırarak tüm caption'ı tek bir satırda birleştir
            caption = caption.replace('\n', ' ')
            
            # Gereksiz boşlukları kaldır
            caption = re.sub(r'\s+', ' ', caption).strip()
            
            # Büyük/küçük harf duyarlılığını kaldır
            caption = caption.lower()
        return caption