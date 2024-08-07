# Git Workflow

The project uses the following Git workflow:

- **main**: Production code
- **development**: Development branch
- **feature/{number}-{name}**: Branches for developing new features
- **bugfix/{number}-{name}**: Branches for fixing bugs during development
- **hotfix/{number}-{name}**: Branches for fixing bugs in production
- **release/{version}**: Branches for final testing before production release

## Getting Started

1. Fork the repository to your GitHub account.
2. Clone your forked repository to your local machine.
```sh
   git clone https://github.com/your-username/your-project-name.git
```

Navigate to the project directory.
```sh
cd your-project-name
```

Add the original repository as a remote called upstream.
```sh
git remote add upstream https://github.com/original-username/original-repo-name.git
```

## Steps

1. **To add a new feature:**

    ```sh
    git checkout development
    git pull upstream development

    git checkout -b feature/{number}-{name}
    # Example:
    # git checkout -b feature/001-login-system
    # git checkout -b feature/002-workspace-system
    # Develop and commit your code
    git add .
    git commit -m "Description of the feature"
    git push origin feature/{number}-{name}
    # Example:
    git push origin feature/001-login-system
    git push origin feature/002-workspace-system

    create pull request
    ```

2. **To fix a bug during development:**

    ```sh
    git checkout development
    git pull upstream development

    git checkout -b bugfix/{number}-{name}
    # Example:
    # git checkout -b bugfix/001-fix-login-error
    # git checkout -b bugfix/002-correct-date-format
    # Fix the bug
    git add .
    git commit -m "Description of the bug fix"
    git push origin bugfix/{number}-{name}
    # Example:
    git push origin bugfix/001-login-error
    git push origin bugfix/002-correct-date-format

    create pull request
    ```

3. **To fix a bug in production:**

    ```sh
    git checkout main
    git pull upstream main

    git checkout -b hotfix/{number}-{name}
    # Example:
    # git checkout -b hotfix/001-login-crash
    # Fix the bug
    git add .
    git commit -m "Description of the bug fix"
    git push origin hotfix/{number}-{name}
    # Example:
    git push origin hotfix/001-login-crash

    create pull request
    ```

Creating Pull request

1. **Pull Request**: Go to your fork on GitHub and click the `Compare & pull request` button.

2. **Details**: Write a description of your pull request and add any necessary details.

3. **Create**: Click the `Create pull request` button to submit your pull request.

Congratulations! You've successfully created a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
