# Godbolt Compiler Explorer MCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides access to the [Godbolt Compiler Explorer](https://godbolt.org) REST API endpoints. Built with the [FastMCP](https://gofastmcp.com/getting-started/welcome) Python library.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd godbolt-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Standalone Usage

Run the MCP server directly:

```bash
python godbolt_mcp.py
```

### Adding to MCP-Compatible Agents

Add the server to your MCP configuration (using virtual environment Python):

```json
{
  "mcpServers": {
    "godbolt-compiler-explorer": {
      "command": "/absolute/path/to/godbolt-mcp/venv/bin/python",
      "args": ["/absolute/path/to/godbolt-mcp/godbolt_mcp.py"]
    }
  }
}
```

**Note**: Replace `/absolute/path/to/godbolt-mcp` with the actual absolute path to your installation directory.

## Available Tools

### Resources (Read-only access)
- `resource://languages` - List all supported programming languages
- `resource://compilers/{language_id}` - Get available compilers for a specific language
- `resource://libraries/{language_id}` - Get available libraries for a specific language
- `resource://formats` - List available code formatters
- `resource://asm/{instruction_set}/{opcode}` - Get assembly instruction documentation
- `resource://version` - Get Compiler Explorer version information

### Tools (Actions)
- `compile_code(compiler_id, source, user_arguments=None, files=None, libraries=None)` - Compile source code
- `compile_cmake(compiler_id, source, user_arguments=None, files=None, libraries=None)` - Compile CMake project
- `format_code(formatter, source)` - Format source code

## Examples

The `examples/` folder contains sample source files you can use to test the MCP server:

- `hello.cpp` - Simple C++ "Hello World" program
- `hello.rs` - Simple Rust "Hello World" program

Try these prompts with MCP-compatible agents to generate assembly code for the example files:

**For C++ example:**
```
Compile the hello.cpp file from the examples folder with GCC and show me the exact generated assembly code with optimization level -O2.
```

**For Rust example:**
```
Compile the hello.rs file from the examples folder with the latest Rust compiler and show me the exact generated assembly code with release optimizations.
```

## Dependencies

- `fastmcp>=0.2.0` - MCP server framework
- `httpx>=0.25.0` - HTTP client for API requests
