"""
Godbolt Compiler Explorer MCP Server
Provides access to the Compiler Explorer API endpoints via MCP protocol.
"""

import httpx
from fastmcp import FastMCP

mcp = FastMCP("godbolt-compiler-explorer")

BASE_URL = "https://godbolt.org"
HEADERS = {"Accept": "application/json"}

@mcp.resource("resource://languages")
def get_languages():
    """Get a list of currently supported languages from Godbolt Compiler Explorer.

    For language-specific compilers, use: resource://compilers/{language_id}
    For language-specific libraries, use: resource://libraries/{language_id}
    """
    response = httpx.get(f"{BASE_URL}/api/languages", headers=HEADERS)
    response.raise_for_status()
    return response.json()

@mcp.resource("resource://compilers/{language_id}")
def get_compilers(language_id: str):
    """Get a list of compilers available for a specific language.
    
    Args:
        language_id: The language identifier (e.g., 'c++', 'rust', 'python')
    """
    response = httpx.get(f"{BASE_URL}/api/compilers/{language_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

@mcp.resource("resource://libraries/{language_id}")
def get_libraries(language_id: str):
    """Get available libraries and versions for a specific language.
    
    Args:
        language_id: The language identifier (e.g., 'c++', 'rust', 'python')
    """
    response = httpx.get(f"{BASE_URL}/api/libraries/{language_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

@mcp.tool
def compile_code(
    compiler_id: str,
    source: str,
    user_arguments: str | None = None,
    files: list[dict] | None = None,
    libraries: list[dict] | None = None
):
    """Compile source code using the specified compiler.
    
    To obtain a valid compiler id, always use resource://compilers/{language_id}
    To obtain a valid librariy id, always use resource://libraries/{language_id}

    Important: If in doubt about which compiler or library version should be used,
    use the latest stable version available. You must inform the user about the version used.

    Args:
        compiler_id: The compiler identifier
        source: The source code to compile
        user_arguments: Compiler flags
        files: List of additional source files with 'filename' and 'contents' keys
        libraries: List of libraries with 'id' and 'version' keys
    """
    payload = {
        "source": source,
        "options": {
            "userArguments": user_arguments or "",
            "libraries": libraries or []
        },
        "files": files or []
    }
    
    response = httpx.post(f"{BASE_URL}/api/compiler/{compiler_id}/compile", json=payload)
    response.raise_for_status()
    return response.text

@mcp.tool
def compile_cmake(
    compiler_id: str,
    source: str,
    user_arguments: str | None = None,
    files: list[dict] | None = None,
    libraries: list[dict] | None = None
):
    """Compile a CMake project using the specified compiler.
    
    To obtain a valid compiler id, always use resource://compilers/{language_id}
    To obtain a valid librariy id, always use resource://libraries/{language_id}

    Important: If in doubt about which compiler or library version should be used,
    use the latest stable version available. You must inform the user about the version used.

    Args:
        compiler_id: The compiler identifier
        source: The source code to compile
        user_arguments: Compiler flags
        files: List of additional source files with 'filename' and 'contents' keys
        libraries: List of libraries with 'id' and 'version' keys
    """
    payload = {
        "source": source,
        "options": {
            "userArguments": user_arguments or "",
            "libraries": libraries or []
        },
        "files": files or []
    }
    
    response = httpx.post(f"{BASE_URL}/api/compiler/{compiler_id}/cmake", json=payload)
    response.raise_for_status()
    return response.text

@mcp.resource("resource://formats")
def get_formatters():
    """Get a list of available code formatters."""
    response = httpx.get(f"{BASE_URL}/api/formats", headers=HEADERS)
    response.raise_for_status()
    return response.json()

@mcp.tool
def format_code(
    formatter: str,
    source: str
):
    """Format source code using the specified formatter.
    
    Args:
        formatter: The formatter identifier
        source: The source code to format
    """
    payload = {
        "source": source
    }
    
    response = httpx.post(f"{BASE_URL}/api/format/{formatter}", json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("answer")

@mcp.resource("resource://asm/{instruction_set}/{opcode}")
def get_instruction_info(instruction_set: str, opcode: str):
    """Get documentation for a specific assembly instruction.
    
    Args:
        instruction_set: The instruction set (e.g., 'x86', 'arm')
        opcode: The instruction opcode
    """
    response = httpx.get(f"{BASE_URL}/api/asm/{instruction_set}/{opcode}")
    response.raise_for_status()
    return response.text

@mcp.resource("resource://version")
def get_version():
    """Get the version information of the Compiler Explorer instance."""
    response = httpx.get(f"{BASE_URL}/api/version", headers=HEADERS)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    mcp.run()
