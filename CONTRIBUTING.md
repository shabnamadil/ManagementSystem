# Git Workflow

The project uses the following Git workflow:

- **main**: Production code
- **development**: Development branch
- **feature/{name}**: Branches for developing new features
- **bugfix/{name}**: Branches for fixing bugs during development
- **hotfix/{name}**: Branches for fixing bugs in production
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

## Working on Issues

### Creating a Feature Branch
Ensure you are on the development branch and it's up to date.
```sh
git checkout development
git pull upstream development
```

## Steps

1. **To add a new feature:**

    ```sh
    git checkout development
    git pull origin development
    git checkout -b feature/{name}
    # Example:
    # git checkout -b feature/login-system
    # Develop and commit your code
    git add .
    git commit -m "Description of the feature"
    git checkout development
    git merge feature/{name}
    # Example:
    # git merge feature/login-system
    git push origin development
    ```

2. **To fix a bug during development:**

    ```sh
    git checkout development
    git pull origin development
    git checkout -b bugfix/{name}
    # Example:
    # git checkout -b bugfix/login-error
    # Fix the bug
    git add .
    git commit -m "Description of the bug fix"
    git checkout development
    git merge bugfix/{name}
    # Example:
    # git merge bugfix/login-error
    git push origin development
    ```

3. **To prepare for a production release:**

    ```sh
    git checkout development
    git pull origin development
    git checkout -b release/{version}
    # Example:
    # git checkout -b release/1.0.0
    # After testing and fixing
    git checkout main
    git merge release/{version}
    # Example:
    # git merge release/1.0.0
    git push origin main
    ```

4. **To fix a bug in production:**

    ```sh
    git checkout main
    git pull origin main
    git checkout -b hotfix/{name}
    # Example:
    # git checkout -b hotfix/login-crash
    # Fix the bug
    git add .
    git commit -m "Description of the bug fix"
    git checkout main
    git merge hotfix/{name}
    # Example:
    # git merge hotfix/login-crash
    git push origin main
    ```

Creating Pull request

1. **Pull Request**: Go to your fork on GitHub and click the `Compare & pull request` button.

2. **Details**: Write a description of your pull request and add any necessary details.

3. **Create**: Click the `Create pull request` button to submit your pull request.

Congratulations! You've successfully created a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
