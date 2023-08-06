import os

# Save yamls in the current directory
namespace = 'franklab'
namespace_filename = f"{namespace}.namespace.yaml"
extension_filename = f"{namespace}.extensions.yaml"

yaml_dir = os.path.dirname(__file__)
namespace_path = os.path.join(yaml_dir, namespace_filename)
extension_path = os.path.join(yaml_dir, extension_filename)
