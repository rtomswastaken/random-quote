# Hands-On Docker Workshop: Python Random Quote Generator

Welcome to your hands-on Docker workshop! In this tutorial, you will take a working Python terminal application and learn how to containerize it with Docker from scratch.

> [!IMPORTANT]
> **No Dockerfile is included in this repository.**  
> The entire purpose of this workshop is for you to learn by writing the `Dockerfile` yourself following the guided exercises below!

---

## Part 1 — What We’re Building

We have an interactive Python terminal application: the **Random Quote Generator**.

First, we will run the application directly on our host computer. Then, we will package it and all of its dependencies into a self-contained **Docker Image** and run it inside an isolated **Docker Container**.

Here is the journey we will take:

```text
Python App (app.py + quotes.json)
       ↓
Dependencies (requirements.txt: rich & pyfiglet)
       ↓
Dockerfile (Recipe written by you)
       ↓
Docker Image (Portable, packaged environment)
       ↓
Docker Container (Running instance of the application)
```

---

## Part 2 — Run It Normally

Before working with Docker, let's run the project the traditional way directly on your computer.

### Step 1: Install Dependencies
Install the required third-party libraries (`rich` and `pyfiglet`):

```bash
pip install -r requirements.txt
```

### Step 2: Run the App
Launch the application:

```bash
python app.py
```

Try pressing `q` to get a quote, `h` for help, and `x` to exit.

### Understanding Where Everything Lives

Notice that Python, `rich`, and `pyfiglet` are currently installed directly on your personal computer:

```text
Your Computer
├── Python
├── rich
├── pyfiglet
└── app.py
```

Later, when we package this into Docker, everything will live safely inside an isolated container:

```text
Docker Container
├── Python
├── rich
├── pyfiglet
└── app.py
```

---

## Part 3 — Why Docker?

Have you ever heard someone say: *"It works on my machine!"*?

This happens all the time in software development. For example:

```text
Student A                       Student B
Python 3.12                     Python 3.10
rich installed                  rich missing
pyfiglet installed              pyfiglet missing
       ↓                               ↓
   ✅ Works                         ❌ Error
```

Student A's computer has the right versions of Python and libraries installed, but Student B's computer does not.

### How Docker Solves This

**Docker** packages an application together with everything it needs to run:
* The exact operating system files
* The exact Python runtime version
* The exact libraries and dependencies
* Your code and assets

Because the application runs inside this isolated container, it runs identically on any computer that has Docker installed—whether it is macOS, Windows, Linux, or a cloud server.

---

## Part 4 — The Dockerfile

A **Dockerfile** is a plain text file containing step-by-step instructions that Docker reads to assemble an image.

You are going to create this file yourself! In your terminal, run:

```bash
touch Dockerfile
```

Now let's examine the essential Dockerfile instructions you will need:

### 1. `FROM`
Specifies the base image to build upon. Every Dockerfile starts with `FROM`.
```dockerfile
FROM python:3.12-slim
```
*Why?* We do not want to build an operating system and install Python from scratch. `python:3.12-slim` is an official, lightweight Linux image that already has Python 3.12 installed.

### 2. `WORKDIR`
Sets the working directory inside the container for all subsequent commands.
```dockerfile
WORKDIR /app
```
*Why?* It acts like `mkdir /app && cd /app` inside the container. This keeps our project files organized in one place rather than in the root folder.

### 3. `COPY`
Copies files or directories from your local computer into the container's file system.
```dockerfile
COPY requirements.txt .
```
*Why?* The container starts empty. We must copy our files from our computer into the container. The `.` refers to the current working directory inside the container (`/app`).

### 4. `RUN`
Executes commands during the image build process (usually used to install software and packages).
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
*Why?* This runs `pip install` inside the container image so that `rich` and `pyfiglet` are baked into the image. `--no-cache-dir` keeps the image size small.

### 5. `CMD`
Specifies the default command that runs when a container starts up from the image.
```dockerfile
CMD ["python", "app.py"]
```
*Why?* Unlike `RUN` (which executes while building the image), `CMD` executes when you actually launch the container with `docker run`.

---

## Part 5 — Your First Dockerfile (Hands-On Exercise)

Now it is your turn to write the Dockerfile!

### Your Task
Open the empty `Dockerfile` you created in your code editor. Write the instructions to:

1. Use Python 3.12 (`python:3.12-slim`) as the base image.
2. Set `/app` as the working directory inside the container.
3. Copy `requirements.txt` into the container.
4. Install the requirements using `pip install --no-cache-dir -r requirements.txt`.
5. Copy `app.py` into the container.
6. Copy `quotes.json` into the container.
7. Run `python app.py` when the container starts.

Here is a template to guide you:

```dockerfile
# Choose a Python base image
# Set the working directory
# Copy requirements.txt
# Install dependencies
# Copy application files
# Run the application
```

Take a few minutes to write this out yourself before looking below!

---

### Solution — Check After Attempting

> [!NOTE]
> Only check this solution after you have attempted to write the Dockerfile yourself!

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY quotes.json .
CMD ["python", "app.py"]
```

Save your `Dockerfile`.

---

## Part 6 — Build the Docker Image

Now that you have written your `Dockerfile`, ask Docker to build an image from it:

```bash
docker build -t random-quote .
```

Let's break down this command:
* `docker build`: The command that instructs Docker to build an image.
* `-t random-quote`: The **tag** (name) you are giving to your image.
* `.`: The **build context** (the current directory where Docker will find your `Dockerfile` and files).

### Inspect Your Images
Once the build completes, list the images stored on your computer:

```bash
docker images
```

You should see `random-quote` listed in the output with its size and Image ID.

> **What is an Image?**  
> An image is a read-only, self-contained template containing your code, Python runtime, libraries, and system tools. Think of it as a snapshot ready to run.

---

## Part 7 — Run the Container

Because our Quote Generator is interactive and waits for terminal input (`q`, `h`, `x`), we must run the container in interactive mode with a terminal attached:

```bash
docker run -it random-quote
```

### What does `-it` mean?
* `-i` (**interactive**): Keeps `STDIN` open so you can type input into the program.
* `-t` (**pseudo-TTY**): Allocates a terminal interface so you see colors, banners, and prompts.

You should now see the ASCII title banner and command prompt inside the container:
```text
q - Get a random quote
h - Show help
x - Exit
> q
```

Type `q` to see a quote, and `x` to exit. You just ran your Python application completely inside an isolated Docker container!

---

## Part 8 — Image vs. Container

A common point of confusion for beginners is the difference between an Image and a Container:

```text
Dockerfile
   ↓ docker build
Image
   ↓ docker run
Container
```

### The Recipe Analogy
* **Dockerfile** = The **Recipe** (the instructions).
* **Image** = The **Prepared Package** (the cake mix or frozen meal).
* **Container** = The **Running Application** (the hot, ready meal on your table).

### Comparing the Commands

* `docker images`: Shows all stored images on your machine.
* `docker ps`: Shows currently **running** containers.
* `docker ps -a`: Shows **all** containers (both running and stopped).

Try running each of these commands in your terminal to see the difference.

---

## Part 9 — Container Management

Let's learn how to inspect, stop, and clean up containers.

### 1. View stopped containers
After you exit `app.py`, the container stops:
```bash
docker ps -a
```

### 2. Give your container a friendly name
By default, Docker assigns random names like `sleepy_archimedes`. You can assign a custom name using `--name`:
```bash
docker run --name quote-app -it random-quote
```

### 3. Stop a running container
If a container is running in the background:
```bash
docker stop <container_name_or_id>
```

### 4. Restart a stopped container
```bash
docker start -ai quote-app
```

### 5. Remove a container
Once you are done with a container, clean it up:
```bash
docker rm quote-app
```

> [!TIP]
> You can also automatically remove a container when it exits by adding `--rm`:  
> `docker run --rm -it random-quote`

---

## Part 10 — Make a Change (Code Update Challenge)

What happens when you modify your Python code? Let's find out!

### Challenge: Add the `a` Command
Open `app.py` in your editor. Add an `a` command that prints all quotes in `quotes.json`:

```python
elif command == "a":
    for q in quotes:
        print(f'"{q["quote"]}" — {q["author"]}')
```

Also add `a - Show all quotes` to `show_help()`.

### The Lesson: Image Immutability
Now, run your container again **without rebuilding**:
```bash
docker run -it random-quote
```
Type `h`. Notice that your new `a` command is **NOT** there!

**Why?**  
The Docker image contains the **old snapshot** of the application from when you ran `docker build`. Docker images do not automatically update when you edit files on your computer.

### The Solution: Rebuild the Image
Whenever you change your code or dependencies, you must rebuild:

```text
Change code
    ↓
Rebuild image (docker build -t random-quote .)
    ↓
Create new container (docker run -it random-quote)
```

1. Rebuild the image:
   ```bash
   docker build -t random-quote .
   ```
2. Run the updated container:
   ```bash
   docker run -it random-quote
   ```
3. Type `a` to see your new feature in action!

---

## Part 11 — Publishing to GitHub

Once you finish your project and want to publish your code to GitHub:

### Step 1: Initialize Git and Commit Your Work
```bash
git init
git add .
git commit -m "Add random quote Docker project"
```

* `git init`: Initializes a Git repository in the project folder.
* `git add .`: Stages all files (`app.py`, `quotes.json`, `requirements.txt`, `.dockerignore`, `.gitignore`, `README.md`, and your `Dockerfile`).
* `git commit -m "..."`: Commits your staged changes with a descriptive message.

### Step 2: Push to Your GitHub Account
Create a new, empty repository on [GitHub](https://github.com/new) named `random-quote-docker`, then run:

```bash
git remote add origin https://github.com/<YOUR_USERNAME>/random-quote-docker.git
git branch -M main
git push -u origin main
```

* `git remote add origin <url>`: Connects your local repository to your remote GitHub repository.
* `git branch -M main`: Renames the default branch to `main`.
* `git push -u origin main`: Uploads your commits to GitHub and sets upstream tracking.

*(Replace `<YOUR_USERNAME>` with your actual GitHub username).*

---

## Part 12 — Final Challenge

Test your mastery by following this end-to-end checklist:

- [ ] 1. Run the Python app normally on your machine with `python app.py`.
- [ ] 2. Create the `Dockerfile` yourself using the instructions in Part 5.
- [ ] 3. Build your Docker image: `docker build -t random-quote .`.
- [ ] 4. Run the container interactively: `docker run -it random-quote`.
- [ ] 5. Make a code change in `app.py`.
- [ ] 6. Rebuild the image with the new change.
- [ ] 7. Run the updated container and verify the change.
- [ ] 8. Push the completed project to your GitHub profile.

---

## Docker Command Cheat Sheet

| Command | Description |
| :--- | :--- |
| `docker build -t random-quote .` | Build an image named `random-quote` from the Dockerfile in the current directory |
| `docker images` | List all Docker images stored on your computer |
| `docker run -it random-quote` | Run a container interactively with a terminal attached |
| `docker ps` | List all currently running containers |
| `docker ps -a` | List all containers (running and stopped) |
| `docker stop <container>` | Stop a running container |
| `docker start <container>` | Start a stopped container |
| `docker rm <container>` | Remove a stopped container |
| `docker rmi <image>` | Remove an image from your computer |
