import subprocess
import os

def create_dockerfile():  # Create Multiple Dockerfiles
    print("=== Dockerfile Creator ===")
    num_files = int(input("How many Dockerfiles do you want to create? "))

    for i in range(num_files):
        print(f"\n--- Dockerfile {i+1} ---")
        save_path = input("Enter the full path to save this Dockerfile: ")

        print("Enter the contents of the Dockerfile line by line.")
        print("Type 'END' when you're done.\n")

        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)

        try:
            with open(save_path, 'w') as f:
                f.write('\n'.join(lines))
            print(f"✅ Dockerfile {i+1} saved at: {save_path}")
        except Exception as e:
            print(f"❌ Error saving Dockerfile {i+1}: {e}")


def build_docker_images():  # 4)Build Multiple Docker Images:
    print("=== Docker Image Builder ===")
    num_images = int(input("How many images do you want to build? "))
    
    for i in range(num_images):
        print(f"\nBuilding image {i+1}...")
        dockerfile_path = input(f"Enter the full path to the Dockerfile for image {i+1}: ")
        image_name = input(f"Enter image name (e.g., myapp) for image {i+1}: ")
        image_tag = input(f"Enter tag (e.g., latest) for image {i+1}: ")

        # Get directory from Dockerfile path
        dockerfile_dir = os.path.dirname(dockerfile_path)
        
        # Build command
        cmd = [
            "docker", "build",
            "-f", dockerfile_path,
            "-t", f"{image_name}:{image_tag}",
            dockerfile_dir
        ]

        print(f"\nRunning command: {' '.join(cmd)}\n")
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Docker image '{image_name}:{image_tag}' built successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Docker image. Error: {e}")

def list_docker_images():
    print("=== List of Docker Images ===")
    
    try:
        result = subprocess.run(["docker", "images"], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to list Docker images. Error: {e}")

def get_used_ports():
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Ports}}"],
            check=True, capture_output=True, text=True
        )
        ports = set()
        for line in result.stdout.strip().splitlines():
            if "->" in line:
                mappings = line.split(",")
                for m in mappings:
                    parts = m.strip().split("->")
                    host_part = parts[0].strip()
                    if ":" in host_part:
                        host_port = host_part.split(":")[-1]
                        ports.add(int(host_port))
        return ports
    except Exception as e:
        print(f"❌ Failed to get used ports: {e}")
        return set()

def run_multiple_containers():
    print("=== Run Multiple Docker Containers ===")
    num_containers = int(input("How many containers do you want to run? "))
    
    base_port = 5000
    used_ports = get_used_ports()

    for i in range(num_containers):
        print(f"\nRunning container {i+1}...")
        container_name = input(f"Enter container name for container {i+1}: ")
        image_name = input(f"Enter image name to use (e.g., myapp) for container {i+1}: ")
        image_tag = input(f"Enter image tag (e.g., latest) for container {i+1}: ")

        # Find next available host port
        while base_port in used_ports:
            base_port += 1

        host_port = base_port
        used_ports.add(host_port)  # Reserve it

        cmd = [
            "docker", "run", "-d",
            "-p", f"{host_port}:5000",
            "--name", container_name,
            f"{image_name}:{image_tag}"
        ]

        print(f"\nRunning command: {' '.join(cmd)}\n")

        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Container '{container_name}' is running at http://localhost:{host_port}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run container. Error: {e}")



def list_running_containers():
    print("=== Running Docker Containers ===")
    
    try:
        result = subprocess.run(["docker", "ps"], check=True, capture_output=True, text=True)
        print(result.stdout if result.stdout.strip() else "No running containers.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to list running containers. Error: {e}")

def stop_container():
    print("=== Stop a Docker Container ===")
    choice = input("Do you want to stop a container? (yes/no): ").strip().lower()

    if choice != "yes":
        print("Skipping container stop step.")
        return

    container_name = input("Enter the container name to stop: ")

    cmd = ["docker", "stop", container_name]

    print(f"\nStopping container: {container_name}\n")

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Container '{container_name}' stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stop container. Error: {e}")

def search_docker_image():
    print("=== Search for a Docker Image ===")
    choice = input("Do you want to search for a Docker image? (yes/no): ").strip().lower()

    if choice != "yes":
        print("Skipping image search step.")
        return

    image_query = input("Enter image name or tag to search: ").strip()

    if not image_query:
        print("⚠️ No search term provided. Skipping search.")
        return

    cmd = ["docker", "search", image_query]

    print(f"\nSearching Docker Hub for: {image_query}...\n")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to search Docker Hub. Error: {e}")



def main():
    print("=== Docker Automation Menu ===")
    print("1. Create Dockerfiles")
    print("2. Build Docker Images")
    print("3. List Docker Images")
    print("4. Run Multiple Containers")
    print("5. List Running Containers")
    print("6. Stop a Container")
    print("7. Search for Docker Images")
    print("0. Exit")

    while True:
        choice = input("\nEnter your choice (0-7): ").strip()

        if choice == "1":
            create_dockerfile()
        elif choice == "2":
            build_docker_images()
        elif choice == "3":
            list_docker_images()
        elif choice == "4":
            run_multiple_containers()
        elif choice == "5":
            list_running_containers()
        elif choice == "6":
            stop_container()
        elif choice == "7":
            search_docker_image()
        elif choice == "0":
            print("Exiting. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select a valid option.")

# Run the interactive menu
main()

