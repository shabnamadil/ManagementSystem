const BASE_URL = `${location.origin}/api/workspaces/`;
const createWorkspaceForm = document.getElementById('createWorkspaceForm');
const container = document.getElementById('my_workspaces');
const errorWorkspaceCreateMessage = document.getElementById('workspacecreatemessage');
const errorWorkspaceEditMessage = document.getElementById('editMessage');
const createWorkspaceBtn = document.getElementById('createWorkspaceBtn')
const cancelCreate = document.getElementById('cancel-create')

let workspaceCategories = []


document.addEventListener("DOMContentLoaded", () => {
  fetchWorkspaces();
  fetchWorkspaceCategories()
});

async function fetchWorkspaces() {
  const FETCH_URL = `${BASE_URL}`;

  try {
    const response = await fetch(FETCH_URL);
    if (!response.ok) throw new Error('Failed to fetch workspaces');
    const data = await response.json();
    displayWorkspaces(data);
  } catch (error) {
    console.error("Error fetching workspaces:", error);
  }
}

async function fetchWorkspaceCategories() {
  const FETCH_URL = `${BASE_URL}categories/`;

  try {
    const response = await fetch(FETCH_URL);
    if (!response.ok) throw new Error('Failed to fetch workspace categories');
    const data = await response.json();
    workspaceCategories = data

  } catch (error) {
    console.error("Error fetching workspace categories:", error);
  }
}

function displayWorkspaces(workspaces) {
  const workspaceCards = workspaces.map(workspace => createWorkspaceCard(workspace)).join('');
  container.innerHTML = workspaceCards;

  workspaces.forEach(workspace => {
    setWorkspaceInviteForm(workspace);
    setDeleteWorkspaceBtn(workspace);
    setWorkspaceEditForm(workspace)
    if (workspace.workspace_members.length > 0) {
      workspace.workspace_members.forEach(member => {
        setRemoveWorkspaceMemberBtn(workspace, member)
        setWorkspaceMemberRoleChangeForm(workspace, member)
      })
    }

  });
}

function createWorkspaceCard(workspace) {
  const category = workspaceCategories.find(category => category.id === workspace.category);

  return `
    <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6"  id="workspace-item-${workspace.id}">
      <div class="card workspace-item">
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between mt-5">
            <div class="lesson_name">
              <div class="project-block ${category.color}">
                <img src="${category.file}" alt="${category.name}" style="width: 30px; height: 30px;">
              </div>
              <span class="small text-muted project_name fw-bold">${category.name}</span>
              <div class="d-flex align-items-center justify-content-center"> 
                  <a href="${workspace.get_absolute_url}"><h6 class="mb-0 fw-bold fs-6">${workspace.title}</h6></a>
                  <div class="d-flex align-items-center justify-content-center ms-2">
                    <span class="small light-danger-bg  p-1 rounded"><i class="icofont-ui-clock"></i> ${workspace.created_date} </span>
                  </div>
              </div>
            </div>
            <div class="btn-group ms-2" role="group" aria-label="Basic outlined example">
              <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#editworkspace-${workspace.id}">
                <i class="icofont-edit text-success"></i>
              </button>
              <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#deleteworkspace-${workspace.id}">
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
              <span class="avatar rounded-circle text-center pointer sm" data-bs-toggle="modal" data-bs-target="#addUser-${workspace.id}">
                <i class="icofont-ui-add"></i>
              </span>
            </div>
          </div>
         <div class="row g-2 pt-4 mb-2">
            <div class="col-6">
              <div class="d-flex align-items-center">
                <i class="icofont-paper-clip"></i>
                <span class="ms-2">${workspace.workspace_project_count} proyekt</span>
              </div>
            </div>
            <div class="col-6">
              <div class="d-flex align-items-center">
                <i class="icofont-group-students"></i>
                <span class="ms-2">${workspace.members_count} üzv</span>
              </div>
            </div>
            <div class="col-6">
              <div class="d-flex align-items-center">
                <i class="icofont-tasks"></i>
                <span class="ms-2">${workspace.tasks_count} tapşırıq</span>
              </div>
            </div>
            <div class="col-6">
              <div class="d-flex align-items-center">
                <i class="icofont-eye"></i>
                <span class="ms-2">${workspace.status}</span>
              </div>
            </div>

          </div> 
        </div>
      </div>
    </div>
  `;
}

async function createWorkspace(formData) {
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
      container.innerHTML = createWorkspaceCard(data) + container.innerHTML;
      const createWorkspaceModal = bootstrap.Modal.getInstance(document.getElementById('createworkspace'));
      if (createWorkspaceModal) {
        createWorkspaceModal.hide();
      }
      const successCreateMessageInfoModal = new bootstrap.Modal(document.getElementById('createStaticBackdropLive'));
      successCreateMessageInfoModal.show();

      setTimeout(() => {
        if (successCreateMessageInfoModal) {
          successCreateMessageInfoModal.hide();
        }
      }, 5000);

      createWorkspaceForm.reset();
    } else {
      errorWorkspaceCreateMessage.innerHTML = ''
      errorWorkspaceCreateMessage.innerHTML += '<div id="errorMessage" class="alert alert-danger text-center">Ad əlavə etmək mütləqdir!!!</div>'

      setTimeout(() => {
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
          errorMessage.remove();
        }
      }, 5000);

    }

  } catch (error) {
    errorWorkspaceCreateMessage.innerHTML = `<div id="errorMessage" class="alert alert-danger text-center">Error: ${error.message}</div>`;

    setTimeout(() => {
      const errorMessage = document.getElementById('errorMessage');
      if (errorMessage) {
        errorMessage.remove();
      }
    }, 5000);
  }
}

async function deleteWorkspace(workspace) {
  const url = `${BASE_URL}${workspace.id}/`;
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
      const successDeleteMessageInfoModal = new bootstrap.Modal(document.getElementById('deleteStaticBackdropLive'));
      successDeleteMessageInfoModal.show();

      setTimeout(() => {
        if (successDeleteMessageInfoModal) {
          successDeleteMessageInfoModal.hide();
        }
      }, 5000);
    } else {
      throw new Error('Failed to delete workspace');
    }
    fetchWorkspaces();
  } catch (error) {
    console.log("Error deleting workspace:", error);
  }
}

async function editWorkspace(formData, workspace) {
  const url = `${BASE_URL}${workspace.id}/`
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
      const workspaceCard = document.getElementById(`workspace-item-${workspace.id}`);
      workspaceCard.outerHTML = createWorkspaceCard(data);
      const editWorkspaceModal = bootstrap.Modal.getInstance(document.getElementById(`editworkspace-${workspace.id}`));
      if (editWorkspaceModal) {
        editWorkspaceModal.hide();
      }
      const successEditMessageInfoModal = new bootstrap.Modal(document.getElementById('editStaticBackdropLive'));
      successEditMessageInfoModal.show();

      setTimeout(() => {
        if (successEditMessageInfoModal) {
          successEditMessageInfoModal.hide();
        }
      }, 5000);

    } else {
      
      errorWorkspaceEditMessage.innerHTML = ''
      errorWorkspaceEditMessage.innerHTML += '<div id="editErrorMessage" class="alert alert-danger text-center">Ad əlavə etmək mütləqdir!!!</div>'
      
      setTimeout(() => {
        const errorMessage = document.getElementById('editErrorMessage');
        if (errorMessage) {
          errorMessage.remove();
        }
      }, 5000);

    }

  } catch (error) {
    errorWorkspaceEditMessage.innerHTML = `<div id="editerrorMessage" class="alert alert-danger text-center">Error: ${error.message}</div>`;

    setTimeout(() => {
      const errorMessage = document.getElementById('editErrorMessage');
      if (errorMessage) {
        errorMessage.remove();
      }
    }, 5000);
  }
}

async function changeWorkspaceMemberRole(formData, workspace) {
  const url = `${BASE_URL}member/role/${workspace.id}/`
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

async function workspaceMemberInvite(formData, workspace) {
  const url = `${BASE_URL}member/invite/${workspace.id}/`
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

async function workspaceMemberRemove(memberId, workspace) {
  const url = `${BASE_URL}member/remove/${workspace.id}/`
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

    if (!response.ok) throw new Error('Failed to remove member from workspace');

  } catch (error) {
    console.log(error);
  }
}

function setWorkspaceInviteForm(workspace) {
  const workspaceMemberInviteForm = document.getElementById(`workspaceMemberInviteForm-${workspace.id}`)
  workspaceMemberInviteForm.addEventListener('submit', function (e) {
    e.preventDefault()
    workspaceMemberInvite((new FormData(workspaceMemberInviteForm)), workspace)
    workspaceMemberInviteForm.reset()
  })
}

function setDeleteWorkspaceBtn(workspace) {
  const deleteWorkspaceBtn = document.getElementById(`deleteworkspace-${workspace.id}`)
  deleteWorkspaceBtn.addEventListener('submit', function (e) {
    e.preventDefault()
    deleteWorkspace(workspace)
  })
}

function setCancelWorkspaceEditBtn(workspace, editWorkspaceForm) {
  const cancelEditWorkspaceBtn = document.getElementById(`cancel-edit-${workspace.id}`)
  cancelEditWorkspaceBtn.addEventListener('click', function (e) {
    e.preventDefault()
    editWorkspaceForm.reset()
  })
}

function setCancelWorkspaceMemberRoleChangeBtn(roleChangeForm, member) {
  const cancelRoleChangeBtn = document.getElementById(`cancelRoleChange-${member.id}`)
  
  cancelRoleChangeBtn.addEventListener('click', function (e) {
    e.preventDefault()
    roleChangeForm.reset()
  })
}

function setRemoveWorkspaceMemberBtn(workspace, member) {
  const removeBtn = document.getElementById(`remove-member-${member.id}`)
  removeBtn.addEventListener('click', function(e) {
    e.preventDefault()
    workspaceMemberRemove(member.id, workspace)
  })
}

function setWorkspaceEditForm(workspace) {
  const editWorkspaceForm = document.getElementById(`editWorkspaceForm-${workspace.id}`)
  editWorkspaceForm.addEventListener('submit', function (e) {
    e.preventDefault()
    editWorkspace((new FormData(editWorkspaceForm)), workspace)
  })
  if (editWorkspaceForm) {
    setCancelWorkspaceEditBtn(workspace, editWorkspaceForm)
  }
}

function setWorkspaceMemberRoleChangeForm(workspace, member) {
  
  const roleChangeForm = document.getElementById(`editWorkspaceMemberRole-${member.id}`)
  
  roleChangeForm.addEventListener('submit', function (e) {
    e.preventDefault()
    changeWorkspaceMemberRole((new FormData(roleChangeForm)), workspace)
  })
  if (roleChangeForm) {
    setCancelWorkspaceMemberRoleChangeBtn(roleChangeForm, member)
  }
}

createWorkspaceForm.addEventListener('submit', function (e) {
  e.preventDefault();
  createWorkspace(new FormData(createWorkspaceForm));
});

cancelCreate.addEventListener('click', function(e) {
  e.preventDefault()
  createWorkspaceForm.reset()
})