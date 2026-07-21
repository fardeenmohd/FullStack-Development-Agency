import os
import json
import sys
import shutil
from local_llm import generate_local_code

enterprise_persona = """
You are an expert Java Developer specializing in clean, compilable Spring Boot 3 applications.
Your job is to read a system architecture blueprint and generate a robust, error-free enterprise backend codebase.

You must output a strictly formatted JSON object containing:
1. "files": An array of objects, where each object has:
   - "path": The target filename (e.g., "pom.xml", "src/main/java/com/app/Application.java")
   - "code": The full string content of the file.

CRITICAL SPRING BOOT 3 COMPILATION RULES:
1. ALL classes, entities, repositories, and controllers MUST be declared as `public` (e.g., `public class User`, `public interface UserRepository`).
2. You MUST include ALL necessary imports in every file:
   - `import jakarta.persistence.*;` (NEVER use `javax.persistence.*`).
   - `import jakarta.validation.constraints.*;`
   - `import java.util.UUID;`, `import java.util.List;`, `import java.math.BigDecimal;`, `import java.sql.Timestamp;`, `import java.util.Optional;`.
3. Package names MUST be strictly consistent: use `com.app.model`, `com.app.repository`, `com.app.service`, `com.app.controller`. Do NOT use plural `models` or `repositories`.
4. Ensure the `pom.xml` uses `<java.version>17</java.version>`, `spring-boot-starter-parent` version 3.2.0, `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `postgresql`, `spring-boot-starter-validation`, and `lombok`.

CRITICAL: Output ONLY valid JSON. Do not wrap the JSON in markdown code blocks.
"""

def fix_java_imports(code: str) -> str:
    """Automatically injects missing common imports into generated Java code."""
    if not code.strip().startswith("package "):
        return code

    lines = code.split("\n")
    package_line_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("package "):
            package_line_idx = i
            break

    # Check for missing symbols and collect needed imports
    needed_imports = set()
    if "UUID" in code and "import java.util.UUID;" not in code:
        needed_imports.add("import java.util.UUID;")
    if "List" in code and "import java.util.List;" not in code:
        needed_imports.add("import java.util.List;")
    if "BigDecimal" in code and "import java.math.BigDecimal;" not in code:
        needed_imports.add("import java.math.BigDecimal;")
    if "Timestamp" in code and "import java.sql.Timestamp;" not in code:
        needed_imports.add("import java.sql.Timestamp;")
    if "Optional" in code and "import java.util.Optional;" not in code:
        needed_imports.add("import java.util.Optional;")
    if "NotBlank" in code and "import jakarta.validation.constraints.NotBlank;" not in code:
        needed_imports.add("import jakarta.validation.constraints.NotBlank;")
    if "Entity" in code and "import jakarta.persistence.Entity;" not in code:
        needed_imports.add("import jakarta.persistence.Entity;")

    if needed_imports:
        # Insert imports right after the package statement
        insertion_idx = package_line_idx + 1
        lines.insert(insertion_idx, "")
        for imp in sorted(needed_imports):
            lines.insert(insertion_idx + 1, imp)
            insertion_idx += 1

    return "\n".join(lines)

def run_enterprise_agent(blueprint_path: str):
    if not os.path.exists(blueprint_path):
        print(f"❌ Error: {blueprint_path} not found.")
        sys.exit(1)

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)

    print("☕ Enterprise Engineer is designing a clean, compilable Spring Boot backend...")

    user_content = f"""
    Based on the following architecture blueprint, generate a clean, compilation-safe Java Spring Boot backend repository.
    Focus on creating a solid `pom.xml`, standard JPA Entities (`public class`), Spring Data Repositories (`public interface`), Services, and REST Controllers (`public class`).
    
    Blueprint:
    {json.dumps(blueprint_data, indent=2)}
    """

    try:
        generated_payload = generate_local_code(enterprise_persona, user_content)
        files = generated_payload.get("files", [])
        
        base_dir = "../backend-java"
        
        print(f"\n🧹 Cleaning old source files in '{base_dir}'...")
        if os.path.exists(os.path.join(base_dir, "src")):
            shutil.rmtree(os.path.join(base_dir, "src"))
        if os.path.exists(os.path.join(base_dir, "pom.xml")):
            os.remove(os.path.join(base_dir, "pom.xml"))

        print(f"\n🚀 Writing fresh enterprise code to '{base_dir}':")
        
        for file_info in files:
            target_path = os.path.join(base_dir, file_info["path"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            file_code = file_info["code"]
            if file_info["path"].endswith(".java"):
                file_code = fix_java_imports(file_code)
            
            with open(target_path, "w", encoding="utf-8") as code_file:
                code_file.write(file_code)
            print(f"  ✅ Created: {file_info['path']}")
            
        print("\n🎉 Enterprise Backend successfully scaffolded via Local GPU!")

    except Exception as x:
        print(f"❌ Error during local enterprise generation: {x}")
        sys.exit(1)

if __name__ == "__main__":
    run_enterprise_agent("system_blueprint.json")