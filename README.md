
# Cracking AI Engineering – Blog 

Welcome to the repository for my Quarto-based blog.
You can see the live version of the blog [here](https://florianbuetow.github.io/).

---

## Usage

**Prerequisites**:
- A working installation of [Docker Desktop](https://www.docker.com/get-started)
- Bash shell (e.g., Git Bash on Windows)

To build and preview the Quarto blog locally using Docker, follow these steps:

1. **Make the shell scripts executable**:
   Run the following command in the project's root directory to ensure that the shell scripts (`*.sh`) have the correct permissions:
   ```bash
   chmod +x *.sh
   ```

2. **Build and run the Docker image**:
   To build and run the Docker image that sets up the website environment:
   ```bash
   ./build.sh
   ```
3. **Preview the website**:
   Once the environment is set up, you can preview the Quarto blog locally by running:
   ```bash
   ./preview.sh
   ```
   This will build and run a Docker image to preview the rendered website at `http://localhost:8000`.
   
4. **Destroy the Docker images**:
   If you need to remove the existing Docker images, use:
   ```bash
   ./destroy.sh
   ```
