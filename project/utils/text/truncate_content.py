def truncate(description):
    max_words = 3
    words = description.split() if description else None
    if words:
        truncated_words = words[:max_words]
        truncated_content = ' '.join(truncated_words)

        if len(words) > max_words:
            truncated_content += ' ...'  

        return truncated_content