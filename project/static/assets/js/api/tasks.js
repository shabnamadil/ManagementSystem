const BASE_URL = `${location.origin}/api/tasks/`;
const tasks_container = document.getElementById('project_tasks')
const createTaskForm = document.getElementById('createTaskForm');
const cancelTaskCreate = document.getElementById('cancel-task-create')
const sharingTasks = document.getElementById('sharing_tasks')
const day = document.getElementById('day')


document.addEventListener("DOMContentLoaded", () => {
    fetchTasks();
});
  
async function fetchTasks() {
    const FETCH_URL = `${BASE_URL}?project=${project}`;
  
    try {
      const response = await fetch(FETCH_URL);
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();
      displayTasks(data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
}
  
function displayTasks(tasks) {
    const taskCards = tasks.map(task => createTaskCard(task)).join('');
    tasks_container.innerHTML = taskCards;
  
    tasks.forEach(task => {
      setTaskInviteForm(task);
      setDeleteTaskBtn(task);
      setTaskEditForm(task)
      setTaskCompletedBtn(task)
    //   if (workspace.workspace_members.length > 0) {
    //     workspace.workspace_members.forEach(member => {
    //       setRemoveWorkspaceMemberBtn(workspace, member)
    //       setWorkspaceMemberRoleChangeForm(workspace, member)
    //     })
    //   }
  
    });
}

function displaySharingTasks(tasks) {
  const taskCards = tasks.map(task => createTaskCard(task)).join('');
  sharingTasks.innerHTML = taskCards;
  if (taskCards.length > 0) {
    const heading = document.createElement('h2');
    heading.textContent = 'Sharing posts';
    sharingTasks.insertBefore(heading, sharingTasks.firstChild);
  }

  tasks.forEach(task => {
  //   setWorkspaceInviteForm(workspace);
    setDeleteTaskBtn(task);
    setTaskEditForm(task)
    setTaskCompletedBtn(task)
  //   if (workspace.workspace_members.length > 0) {
  //     workspace.workspace_members.forEach(member => {
  //       setRemoveWorkspaceMemberBtn(workspace, member)
  //       setWorkspaceMemberRoleChangeForm(workspace, member)
  //     })
  //   }

  });
}
  
function createTaskCard(task) {
  
    return `
      <div class="col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6"  id="task-item-${task.id}">
        <div class="card task-item">
          <div class="card-body">
            <div class="d-flex align-items-center justify-content-between mt-5">
              <div class="lesson_name">
                <div class="d-flex align-items-center justify-content-center"> 
                    <a href="${task.get_absolute_url}"><h6 class="mb-0 fw-bold fs-6">${task.title}</h6></a>
                    <div class="d-flex align-items-center justify-content-center ms-2">
                      <span class="small light-danger-bg  p-1 rounded"> ${task.priority} </span>
                    </div>
                </div>
              </div>
              <div class="btn-group ms-2" role="group" aria-label="Basic outlined example">
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#edittask-${task.id}">
                  <i class="icofont-edit text-success"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#deletetask-${task.id}">
                  <i class="icofont-ui-delete text-danger"></i>
                </button>
                <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" id="completetask-${task.id}">
                ${task.completed ? '<i class="icofont-check-circled"></i>' : '<i class="icofont-close-line-circled"></i>'}
                </button>
              </div>
            </div>
            <div class="d-flex align-items-center">
              <div class="avatar-list avatar-list-stacked pt-2">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar2.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar1.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar3.jpg" alt="">
                <img class="avatar rounded-circle sm" src="/static/assets/images/xs/avatar4.jpg" alt="">
                <span class="avatar rounded-circle text-center pointer sm" data-bs-toggle="modal" data-bs-target="#addTaskMember-${task.id}">
                  <i class="icofont-ui-add"></i>
                </span>
              </div>
            </div>
           <div class="row g-2 pt-4 mb-2">
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-paper-clip"></i>
                  <span class="ms-2">comments count</span>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-group-students"></i>
                  <span class="ms-2">${task.members_count} üzv</span>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-tasks"></i>
                  <span class="ms-2">${task.subtasks_count} subtasks</span>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center">
                  <i class="icofont-check-alt"></i>
                  <span class="ms-2">${task.completed_percent} %</span>
                </div>
              </div>
            </div> 
          </div>
        </div>
      </div>
    `;
}

async function createTask(formData) {
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
        tasks_container.innerHTML = createTaskCard(data) + tasks_container.innerHTML;
        const createTaskModal = bootstrap.Modal.getInstance(document.getElementById('createtask'));
        if (createTaskModal) {
          createTaskModal.hide();
        }
  
        createTaskForm.reset();
      }
  
    } catch (error) {
        console.log(error);
        
    }
}

async function deleteTask(task) {
    const url = `${BASE_URL}${task.id}/`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  
    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      });
  
      fetchTasks();
    } catch (error) {
      console.log("Error deleting task:", error);
    }
}

async function editTask(formData, task) {
    const url = `${BASE_URL}${task.id}/`
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
        const taskCard = document.getElementById(`task-item-${task.id}`);
        taskCard.outerHTML = createTaskCard(data);
      }
  
    } catch (error) {
        console.log(error);
        
    }
}

async function completeTask(task) {
  const url = `${BASE_URL}completed/${task.id}/`
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  try {
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
    });

    if (response.ok) {
      const data = await response.json();
      const taskCard = document.getElementById(`task-item-${task.id}`);
      taskCard.outerHTML = createTaskCard(data);
    }
    fetchTasks()
  } catch (error) {
      console.log(error);
  }
}

async function taskMemberInvite(formData, task) {
  const url = `${BASE_URL}member/invite/${task.id}/`
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

createTaskForm.addEventListener('submit', function (e) {
    e.preventDefault();
    createTask(new FormData(createTaskForm));
});
  
cancelTaskCreate.addEventListener('click', function(e) {
    e.preventDefault()
    createTaskForm.reset()
})

function setTaskEditForm(task) {
    const ediTaskForm = document.getElementById(`editTaskForm-${task.id}`)
    ediTaskForm.addEventListener('submit', function (e) {
      e.preventDefault()
      editTask((new FormData(ediTaskForm)), task)
    })
    if (ediTaskForm) {
      setCancelTaskEditBtn(task, ediTaskForm)
      ediTaskForm.reset()
    }
}

function setTaskInviteForm(task) {
  const taskMemberInviteForm = document.getElementById(`taskMemberInviteForm-${task.id}`)
  taskMemberInviteForm.addEventListener('submit', function (e) {
    e.preventDefault()
    taskMemberInvite((new FormData(taskMemberInviteForm)), task)
    taskMemberInviteForm.reset()
  })
}

function setDeleteTaskBtn(task) {
    const deleteTaskBtn = document.getElementById(`deletetask-${task.id}`)
    deleteTaskBtn.addEventListener('submit', function (e) {
      e.preventDefault()
      deleteTask(task)
    })
}

function setCancelTaskEditBtn(task, ediTaskForm) {
    const cancelEditTaskBtn = document.getElementById(`cancel-task-edit-${task.id}`)
    cancelEditTaskBtn.addEventListener('click', function (e) {
      e.preventDefault()
      ediTaskForm.reset()
    })
}

function setTaskCompletedBtn(task) {
  const completedTaskBtn = document.getElementById(`completetask-${task.id}`)
  completedTaskBtn.addEventListener('click', function (e) {
    e.preventDefault()
    completeTask(task)
  })
}

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: function(fetchInfo, successCallback, failureCallback) {
          fetch(`${BASE_URL}?date=${fetchInfo}&project=${project}&share_date=${fetchInfo}`)
              .then(response => response.json())
              .then(data => {
                  successCallback(data);
              })
              .catch(error => {
                  failureCallback(error);
              });
      },
      dateClick: function(info) {
        tasks_container.innerHTML 
          fetchTasksForDay(info.dateStr);
          fetchTasksForSharingDay(info.dateStr)
          day.innerHTML = ''
          day.innerHTML += `<h2>${info.dateStr}</h2>`
      }
  });

  calendar.render();
});

function fetchTasksForDay(dateStr) {
  fetch(`${BASE_URL}?date=${dateStr}&project=${project}`)
      .then(response => response.json())
      .then(tasks => {
          displayTasks(tasks);
      });
}

function fetchTasksForSharingDay(dateStr) {
  fetch(`${BASE_URL}?share_date=${dateStr}&project=${project}`)
      .then(response => response.json())
      .then(tasks => {
          displaySharingTasks(tasks);
      })
      .catch(error => {
          console.error('Error fetching tasks for the sharing day:', error);
      });
}


