const BASE_URL = `${location.origin}/api/projects/`;
const project_container = document.getElementById('workspace_projects');
const createProjectForm = document.getElementById('createProjectForm');


document.addEventListener("DOMContentLoaded", () => {
    fetchProjects();
});

async function fetchProjects() {
    const FETCH_URL = `${BASE_URL}?workspace=${workspace}`;
  
    try {
      const response = await fetch(FETCH_URL);
      if (!response.ok) throw new Error('Failed to fetch projects');
      const data = await response.json();
      displayProjects(data);
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
}

function displayProjects(projects) {
    const projectCards = projects.map(project => createProjectCard(project)).join('');
    project_container.innerHTML = projectCards;
  
    projects.forEach(project => {
      setProjectInviteForm(project);
      setDeleteProjectBtn(project);
      setWorkspaceEditForm(project)
      if (project.project_members.length > 0) {
        project.project_members.forEach(member => {
          setRemoveProjectMemberBtn(project, member)
          setProjectMemberRoleChangeForm(project, member)
        })
      }
  
    });
}

function createProjectCard(project) {
  
    return `
      <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6"  id="project-item-${project.id}">
        <div class="card workspace-item">
          <div class="card-body">
            <div class="d-flex align-items-center justify-content-between mt-5">
              <div class="lesson_name">
                <div class="d-flex align-items-center justify-content-center"> 
                    <a href="${project.get_absolute_url}"><h6 class="mb-0 fw-bold fs-6">${project.title}</h6></a>
                    <div class="d-flex align-items-center justify-content-center ms-2">
                      <span class="small light-danger-bg  p-1 rounded"><i class="icofont-ui-clock"></i> ${project.created_date} </span>
                    </div>
                </div>
              </div>
              <div class="btn-group ms-2" role="group" aria-label="Basic outlined example">
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#editproject-${project.id}">
                  <i class="icofont-edit text-success"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#deleteproject-${project.id}">
                  <i class="icofont-ui-delete text-danger"></i>
                </button>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="avatar-list avatar-list-stacked pt-2">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar2.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar1.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar3.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar4.jpg" alt="">
                <span class="avatar rounded-circle text-center pointer sm" data-bs-toggle="modal" data-bs-target="#addProjectMember-${project.id}">
                  <i class="icofont-ui-add"></i>
                </span>
              </div>
            </div>
           <div class="row g-2 pt-4 mb-2">
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-paper-clip"></i>
                  <span class="ms-2">${project.tasks_count} tapşırıq</span>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-group-students"></i>
                  <span class="ms-2">${project.members_count} üzv</span>
                </div>
              </div>
            </div> 
          </div>
        </div>
      </div>
    `;
}

async function createProject(formData) {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(BASE_URL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      });
  
      if (response.ok) {
        const data = await response.json();
        project_container.innerHTML = createProjectCard(data) + project_container.innerHTML;
        createProjectForm.reset()
      }
  
    } catch (error) {
        console.log(error);
        
    }
}

async function deleteProject(project) {
    const url = `${BASE_URL}${project.id}/`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      });
  
      if (response.ok) {
        fetchProjects()
      }
    } catch (error) {
      console.log("Error deleting workspace:", error);
    }
}

async function editProject(formData, project) {
    const url = `${BASE_URL}${project.id}/`
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: formData
      });
  
      if (response.ok) {
        const data = await response.json();
        const projectCard = document.getElementById(`project-item-${project.id}`);
        projectCard.outerHTML = createProjectCard(data);
        const editProjectModal = bootstrap.Modal.getInstance(document.getElementById(`editproject-${project.id}`));
        if (editProjectModal) {
          editProjectModal.hide();
        }
  
      } else {
        
        errorProjectEditMessage.innerHTML = ''
        errorProjectEditMessage.innerHTML += '<div id="editErrorMessage" class="alert alert-danger text-center">Ad əlavə etmək mütləqdir!!!</div>'
  
        setTimeout(() => {
          const errorMessage = document.getElementById('editErrorMessage');
          if (errorMessage) {
            errorMessage.remove();
          }
        }, 5000);
  
      }
  
    } catch (error) {
      errorProjectEditMessage.innerHTML = `<div id="editerrorMessage" class="alert alert-danger text-center">Error: ${error.message}</div>`;
  
      setTimeout(() => {
        const errorMessage = document.getElementById('editErrorMessage');
        if (errorMessage) {
          errorMessage.remove();
        }
      }, 5000);
    }
}

async function projectMemberInvite(formData, project) {
  const url = `${BASE_URL}member/invite/${project.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    });

    if (!response.ok) throw new Error('Failed to send email');

  } catch (error) {
    console.log(error);

  }

}

async function projectMemberRemove(memberId, project) {
  const url = `${BASE_URL}member/remove/${project.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
  const data = {
    member: memberId
  };

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error('Failed to remove member from project');

  } catch (error) {
    console.log(error);
  }
}

async function changeProjectMemberRole(formData, project) {
  const url = `${BASE_URL}member/role/${project.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    });

  } catch (error) {
    console.log(error);
    
  }
}

createProjectForm.addEventListener('submit', function (e) {
    e.preventDefault();
    createProject(new FormData(createProjectForm));
});

function setDeleteProjectBtn(project) {
    const deleteProjectForm = document.getElementById(`deleteproject-${project.id}`)
    deleteProjectForm.addEventListener('submit', function (e) {
      e.preventDefault()
      deleteProject(project)
    })
}

function setCancelProjectEditBtn(project, editPrjectForm) {
    const cancelEditProjectBtn = document.getElementById(`cancel-project-edit-${project.id}`)
    cancelEditProjectBtn.addEventListener('click', function (e) {
      e.preventDefault()
      editPrjectForm.reset()
    })
}

function setCancelProjectMemberRoleChangeBtn(roleChangeForm, member) {
  const cancelRoleChangeBtn = document.getElementById(`cancelRoleChange-${member.id}`)
  
  cancelRoleChangeBtn.addEventListener('click', function (e) {
    e.preventDefault()
    roleChangeForm.reset()
  })
}

function setRemoveProjectMemberBtn(project, member) {
  const removeBtn = document.getElementById(`remove-project-member-${member.id}`)
  removeBtn.addEventListener('click', function(e) {
    e.preventDefault()
    projectMemberRemove(member.id, project)
  })
}

function setWorkspaceEditForm(project) {
    const editProjectForm = document.getElementById(`editProjectForm-${project.id}`)
    editProjectForm.addEventListener('submit', function (e) {
      e.preventDefault()
      editProject((new FormData(editProjectForm)), project)
    })
    if (editProjectForm) {
      setCancelProjectEditBtn(project, editProjectForm)
    }
}

function setProjectInviteForm(project) {
  const projectMemberInviteForm = document.getElementById(`projectMemberInviteForm-${project.id}`)
  projectMemberInviteForm.addEventListener('submit', function (e) {
    e.preventDefault()
    projectMemberInvite((new FormData(projectMemberInviteForm)), project)
    projectMemberInviteForm.reset()
  })
}

function setProjectMemberRoleChangeForm(project, member) {
  const roleChangeForm = document.getElementById(`editProjectMemberRole-${member.id}`)
  roleChangeForm.addEventListener('submit', function (e) {
    e.preventDefault()
    changeProjectMemberRole((new FormData(roleChangeForm)), project)
  })
  if (roleChangeForm) {
    setCancelProjectMemberRoleChangeBtn(roleChangeForm, member)
  }
}