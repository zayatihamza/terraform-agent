# Terraform Agent - CloudStack RAG System

An intelligent Terraform code generation system that uses Retrieval-Augmented Generation (RAG) with Milvus vector database and Groq LLM to automatically generate CloudStack Terraform configurations based on natural language queries.

## 🚀 Features

- **Intelligent Resource Resolution**: Automatically maps natural language queries to CloudStack Terraform resources
- **RAG-Powered Documentation**: Uses vector embeddings to retrieve relevant CloudStack documentation
- **Interactive Field Collection**: Smart prompting for required and optional fields with validation
- **Terraform Validation**: Comprehensive validation including syntax, CLI, and required fields checks
- **Auto-Generated Configurations**: Produces ready-to-use Terraform HCL files
- **Field Suggestions**: Provides examples, defaults, and options for each field
- **Multi-language Support**: French configuration comments and error messages

## 🏗️ Architecture

```
User Query → Resource Resolution → Documentation Retrieval → Field Collection → Validation → Terraform Generation
     ↓              ↓                    ↓                    ↓              ↓              ↓
Natural Language → Milvus Search → Vector Embeddings → Interactive Prompts → HCL Validation → .tf Files
```

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Terraform CLI (optional, for validation)
- Groq API Key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Terraform_agent
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Required
   setx GROQ_API_KEY "your_groq_api_key_here"
   
   # Optional (with defaults)
   setx MILVUS_HOST "localhost"
   setx MILVUS_PORT "19530"
   setx MILVUS_COLLECTION "cloudstack_docs"
   setx GROQ_MODEL "llama-3.3-70b-versatile"
   setx TERRAFORM_VALIDATION "true"
   ```

5. **Start Milvus services**
   ```bash
   docker-compose -f milvus-docker-compose.yml up -d
   ```

## 🎯 Usage

### 1. Data Ingestion (First Time Setup)

Process and ingest CloudStack documentation into Milvus:

```bash
# Clean scraped documentation
python Clean.py

# Ingest documentation into Milvus
python milvus_ingest.py
```

### 2. Generate Terraform Configurations

Run the main RAG agent:

```bash
python milvus_rag_groq.py
```

**Example interaction:**
```
What do you want to provision? I need a virtual machine instance

[Resolved resource] cloudstack_instance
Required fields: ['name', 'service_offering', 'template', 'zone']
Detected optional fields: ['display_name', 'network_id', 'ip_address', 'keypair', 'security_group_ids']

Enter value for 'name' [example=my-vm]: my-web-server
Enter value for 'service_offering' [options=['small', 'medium', 'large']]: small
Enter value for 'template' [example=ubuntu-20.04]: ubuntu-20.04
Enter value for 'zone' [example=zone1]: zone1

Do you want to fill optional fields? (y/N): y
Enter value for 'display_name' [example=My Web Server]: Web Server Instance
...
```

## 📁 Project Structure

```
Terraform_agent/
├── config.py                 # Configuration management
├── Clean.py                  # Documentation cleaning utility
├── milvus_ingest.py         # Milvus data ingestion
├── milvus_rag_groq.py       # Main RAG agent
├── milvus-docker-compose.yml # Milvus services
├── cleaned_docs/            # Processed documentation
├── generated/               # Generated Terraform files
├── volumes/                 # Milvus persistent data
└── venv/                   # Python virtual environment
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | Required | Groq API key for LLM access |
| `MILVUS_HOST` | localhost | Milvus server host |
| `MILVUS_PORT` | 19530 | Milvus server port |
| `MILVUS_COLLECTION` | cloudstack_docs | Milvus collection name |
| `GROQ_MODEL` | llama-3.3-70b-versatile | Groq model to use |
| `TERRAFORM_VALIDATION` | true | Enable Terraform validation |
| `MAX_CONTEXT_CHUNKS` | 8 | Max documentation chunks for context |
| `OUTPUT_DIR` | generated | Directory for generated files |

### Milvus Configuration

The system uses Milvus for vector storage with the following schema:
- **id**: Unique document identifier
- **resource**: CloudStack resource name (e.g., cloudstack_instance)
- **required_fields**: JSON array of required field names
- **text**: Documentation content chunk
- **embedding**: 1024-dimensional vector (BGE-M3 model)

## 🧠 How It Works

### 1. Resource Resolution
- Uses Groq LLM to map natural language to CloudStack resources
- Falls back to fuzzy matching if LLM fails
- Supports queries like "virtual machine", "load balancer", "network"

### 2. Documentation Retrieval
- Searches Milvus vector database for relevant documentation
- Uses BGE-M3 embeddings for semantic search
- Retrieves required fields and optional fields metadata

### 3. Interactive Field Collection
- Prompts user for required fields with validation
- Provides suggestions, examples, and defaults
- Validates field values using LLM and heuristics
- Optionally collects optional fields

### 4. Terraform Generation
- Uses Groq LLM to generate valid HCL code
- Enforces CloudStack provider usage
- Handles missing required fields gracefully

### 5. Validation
- **Syntax Check**: HCL parsing validation
- **Required Fields**: Ensures all required fields are present
- **Terraform CLI**: Runs `terraform validate` if available
- **Comprehensive Reporting**: Shows validation results and suggestions

## 🎯 Supported CloudStack Resources

The system supports all major CloudStack Terraform resources including:

- **Compute**: `cloudstack_instance`, `cloudstack_template`
- **Networking**: `cloudstack_network`, `cloudstack_vpc`, `cloudstack_firewall`
- **Storage**: `cloudstack_volume`, `cloudstack_disk_offering`
- **Security**: `cloudstack_security_group`, `cloudstack_ssh_keypair`
- **Load Balancing**: `cloudstack_loadbalancer_rule`
- **VPN**: `cloudstack_vpn_connection`, `cloudstack_vpn_gateway`
- **And many more...**

## 🔍 Validation Features

### Syntax Validation
- HCL parsing using python-hcl2
- Basic structure validation
- Error detection and reporting

### Required Fields Validation
- Ensures all required fields are provided
- Reports missing fields with suggestions
- Prevents incomplete configurations

### Terraform CLI Validation
- Runs `terraform init` and `terraform validate`
- Uses temporary directories for isolation
- Handles provider configuration automatically

### Comprehensive Reporting
```
📋 Validation Results:
========================================
✅ Overall Status: VALID
✅ HCL Syntax: Syntax valid
✅ Required Fields: All present
✅ Terraform CLI: Terraform validation passed
========================================
```

## 🚀 Generated Output

The system generates clean, production-ready Terraform files:

```hcl
resource "cloudstack_instance" "my-web-server" {
  name             = "my-web-server"
  service_offering = "small"
  template         = "ubuntu-20.04"
  zone             = "zone1"
  display_name      = "Web Server Instance"
  keypair          = "my-keypair"
  security_group_ids = ["sg-12345"]
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Milvus Connection Failed**
   ```bash
   # Check if Milvus is running
   docker-compose -f milvus-docker-compose.yml ps
   
   # Restart services
   docker-compose -f milvus-docker-compose.yml restart
   ```

2. **Groq API Key Missing**
   ```bash
   # Set the API key
   setx GROQ_API_KEY "your_key_here"
   # Restart your terminal/IDE
   ```

3. **No Resources Found**
   ```bash
   # Re-run data ingestion
   python milvus_ingest.py
   ```

4. **Terraform Validation Fails**
   - Check if Terraform CLI is installed
   - Verify CloudStack provider is available
   - Review validation error messages

### Debug Mode

Enable debug logging:
```bash
setx DEBUG_MODE "true"
setx LOG_LEVEL "DEBUG"
```

## 📈 Performance

- **Embedding Model**: BGE-M3 (1024 dimensions)
- **Vector Search**: Cosine similarity with IVF_FLAT index
- **Context Window**: 8 documentation chunks maximum
- **Validation Timeout**: 60 seconds for Terraform CLI validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Milvus**: Vector database for semantic search
- **Groq**: High-performance LLM inference
- **BAAI/BGE-M3**: Embedding model for multilingual support
- **CloudStack**: Infrastructure management platform
- **Terraform**: Infrastructure as Code tool

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in debug mode
3. Open an issue on GitHub
4. Contact the development team

---

**Happy Terraforming! 🚀**
