from flask import Flask, render_template, request, jsonify
import subprocess, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_dockerfile', methods=['POST'])
def create_dockerfile():
    path = request.form['path']
    content = request.form['content']
    try:
        with open(path, 'w') as f:
            f.write(content)
        return jsonify({'status': 'success', 'message': f'Dockerfile saved at {path}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/build_image', methods=['POST'])
def build_image():
    dockerfile_file = request.files.get('dockerfile_file')
    name = request.form['image_name']
    tag = request.form['image_tag']
    if not dockerfile_file:
        return jsonify({'status': 'error', 'message': 'No Dockerfile uploaded.'})
    temp_dir = './temp'
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, 'Dockerfile')
    dockerfile_file.save(temp_path)
    cmd = ['docker', 'build', '-f', temp_path, '-t', f'{name}:{tag}', temp_dir]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': f'Image {name}:{tag} created successfully.', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': e.stderr})

@app.route('/run_container', methods=['POST'])
def run_container():
    name = request.form['container_name']
    image = request.form['image_name']
    tag = request.form['image_tag']
    port = request.form['host_port']
    cmd = ['docker', 'run', '-d', '-p', f'{port}:5000', '--name', name, f'{image}:{tag}']
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        container_id = result.stdout.strip()
        link = f'http://localhost:{port}'
        return jsonify({'status': 'success', 'message': f'Container {name} is running at {link}', 'output': container_id})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': 'Container run failed', 'output': e.stderr})

@app.route('/list_images')
def list_images():
    try:
        result = subprocess.run(['docker', 'images'], check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.stderr})

@app.route('/list_containers')
def list_containers():
    try:
        result = subprocess.run(['docker', 'ps'], check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.stderr})

@app.route('/stop_container', methods=['POST'])
def stop_container():
    container_name = request.form['container_name']
    try:
        result = subprocess.run(['docker', 'stop', container_name], check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': f'Container {container_name} stopped successfully', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': e.stderr})

@app.route('/search_image', methods=['POST'])
def search_image():
    image_name = request.form['search_term']
    try:
        result = subprocess.run(['docker', 'search', image_name], check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'result': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'result': e.stderr})

@app.route('/list_running_containers', methods=['GET'])
def list_running_containers():
    try:
        result = subprocess.run(['docker', 'ps', '--format', '{{.ID}} {{.Names}}'], check=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        containers = []
        for line in lines:
            if line.strip():
                parts = line.split(' ', 1)
                containers.append({'id': parts[0], 'name': parts[1]})
        return jsonify({'status': 'success', 'containers': containers})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'containers': [], 'message': e.stderr})

@app.route('/pull_image', methods=['POST'])
def pull_image():
    image_name = request.form['image_name']
    tag = request.form.get('tag', 'latest')
    image_ref = image_name if not tag else f"{image_name}:{tag}"
    try:
        result = subprocess.run(['docker', 'pull', image_ref], check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': f'Image {image_ref} pulled successfully', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Failed to pull image {image_ref}', 'output': e.stderr})

@app.route('/search_local_images', methods=['POST'])
def search_local_images():
    search_term = request.form['search_term']
    try:
        output = subprocess.check_output(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'], text=True)
        matches = '\n'.join([line for line in output.splitlines() if search_term.lower() in line.lower()])
        return jsonify({'status': 'success', 'result': matches if matches else 'No matches found'})
    except Exception as e:
        return jsonify({'status': 'error', 'result': str(e)})

if __name__ == '__main__':
    app.run(debug=True)