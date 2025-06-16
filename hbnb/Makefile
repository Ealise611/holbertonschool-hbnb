# =============================================================================
# HBnB Project Makefile
# =============================================================================
# 
# This Makefile automates common development tasks for the HBnB project.
# 
# USAGE:
#   make <command>
# 
# EXAMPLES:
#   make help          # Show all available commands
#   make setup         # First-time project setup
#   make test          # Run all tests
#   make run           # Start Flask application
#   make clean         # Clean up temporary files
# 
# REQUIREMENTS:
#   - Python 3.6+ installed
#   - pip package manager
#   - make utility (usually pre-installed on Linux/Mac)
# 
# DAILY WORKFLOW:
#   1. make test       # Test your changes
#   2. make run        # Start the application
#   3. make clean      # Clean up before committing

# TROUBLESHOOTING:
#   - If commands fail, check that Python 3 is installed: python3 --version
#   - On Windows, you might need to install make or use WSL
#   - For permission errors, you might need: sudo make install
# 
# =============================================================================

# =============================================================================
# HBnB Project Makefile
# =============================================================================
# 
# This Makefile automates common development tasks for the HBnB project.
# 
# USAGE:
#   make <command>
# 
# EXAMPLES:
#   make help          # Show all available commands
#   make setup         # First-time project setup
#   make test          # Run all tests
#   make run           # Start Flask application
#   make clean         # Clean up temporary files
# 
# REQUIREMENTS:
#   - Python 3.6+ installed
#   - pip package manager
#   - make utility (usually pre-installed on Linux/Mac)
# 
# FIRST TIME SETUP:
#   1. Clone the repository
#   2. Navigate to project directory: cd hbnb
#   3. Run: make setup
#   4. Start developing!
# 
# DAILY WORKFLOW:
#   1. make test       # Test your changes
#   2. make run        # Start the application
#   3. make clean      # Clean up before committing
# 
# TEAM COLLABORATION:
#   - All team members should use these same commands
#   - Ensures consistent development environment
#   - No need to remember complex command lines
# 
# TROUBLESHOOTING:
#   - If commands fail, check that Python 3 is installed: python3 --version
#   - On Windows, you might need to install make or use WSL
#   - For permission errors, you might need: sudo make install
# 
# =============================================================================

# Variables - Customize these if needed
PYTHON = python3
TEST_DIR = tests
REQUIREMENTS = requirements.txt

# Colors for pretty output (makes terminal output more readable)
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
RED = \033[0;31m
NC = \033[0m # No Color

# Default target - runs when you just type 'make'
# Shows help information with all available commands
help:
	@echo "$(BLUE)╔══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║                    HBnB Project Commands                     ║$(NC)"
	@echo "$(BLUE)╚══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)📦 SETUP COMMANDS:$(NC)"
	@echo "  make install      - Install project dependencies"
	@echo "  make setup        - Complete first-time setup (install + test)"
	@echo "  make venv         - Create virtual environment"
	@echo "  make dev-setup    - Full development environment setup"
	@echo ""
	@echo "$(GREEN)🧪 TESTING COMMANDS:$(NC)"
	@echo "  make test         - Run all tests with detailed output"
	@echo "  make test-quick   - Run tests with minimal output"
	@echo "  make test-models  - Test only model classes (User, Place, etc.)"
	@echo "  make test-facade  - Test only facade functionality"
	@echo ""
	@echo "$(GREEN)🚀 DEVELOPMENT COMMANDS:$(NC)"
	@echo "  make run          - Start Flask application (http://localhost:5000)"
	@echo "  make status       - Show project status and information"
	@echo ""
	@echo "$(GREEN)🧹 CLEANUP COMMANDS:$(NC)"
	@echo "  make clean        - Remove temporary files and cache"
	@echo ""
	@echo "$(YELLOW)💡 EXAMPLES:$(NC)"
	@echo "  New team member:   make dev-setup"
	@echo "  Daily development: make test && make run"
	@echo "  Before commit:     make clean && make test"
	@echo ""
	@echo "$(YELLOW)ℹ️  For more help, check the comments in this Makefile$(NC)"

# =============================================================================
# SETUP COMMANDS
# =============================================================================

# Install project dependencies from requirements.txt
# This is usually the first command you run after cloning the project
install:
	@echo "$(YELLOW)📦 Installing project dependencies...$(NC)"
	@echo "Using Python: $(shell $(PYTHON) --version)"
	$(PYTHON) -m pip install -r $(REQUIREMENTS)
	@echo "$(GREEN)✅ Dependencies installed successfully!$(NC)"
	@echo "$(BLUE)Next steps: Run 'make test' to verify everything works$(NC)"

# Complete project setup - ideal for new team members
# Installs dependencies and runs tests to verify everything works
setup: install test
	@echo "$(GREEN)🎉 Setup complete! Your HBnB project is ready for development.$(NC)"
	@echo "$(BLUE)Try running 'make run' to start the Flask application$(NC)"

# Create Python virtual environment (optional but recommended)
# Virtual environments isolate project dependencies
venv:
	@echo "$(YELLOW)🐍 Creating Python virtual environment...$(NC)"
	$(PYTHON) -m venv venv
	@echo "$(GREEN)✅ Virtual environment created in ./venv/$(NC)"
	@echo "$(YELLOW)To activate it:$(NC)"
	@echo "  Linux/Mac: source venv/bin/activate"
	@echo "  Windows:   venv\\Scripts\\activate"
	@echo "$(BLUE)After activation, run 'make install' to install dependencies$(NC)"

# Complete development environment setup with virtual environment
# Perfect for new developers joining the project
dev-setup: venv
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	@echo "$(BLUE)Remember to activate virtual environment first!$(NC)"
	@echo "Then run: make install && make test"

# =============================================================================
# TESTING COMMANDS
# =============================================================================

# Run all tests with detailed output
# This is the main testing command you'll use most often
test:
	@echo "$(YELLOW)🧪 Running all tests...$(NC)"
	@echo "Testing Task 1: Core Business Logic Classes"
	@echo "============================================"
	$(PYTHON) $(TEST_DIR)/test_runner.py
	@echo "$(GREEN)✅ All tests completed!$(NC)"

# Run tests with minimal output (useful for quick checks)
test-quick:
	@echo "$(YELLOW)🧪 Quick test run...$(NC)"
	@$(PYTHON) $(TEST_DIR)/test_runner.py
	@echo "$(GREEN)✅ Quick test complete!$(NC)"

# Test only the model classes (User, Place, Review, Amenity)
# Useful when you're working specifically on model logic
test-models:
	@echo "$(YELLOW)🧪 Testing model classes...$(NC)"
	$(PYTHON) $(TEST_DIR)/test_models/test_user.py
	$(PYTHON) $(TEST_DIR)/test_models/test_place.py
	$(PYTHON) $(TEST_DIR)/test_models/test_review.py
	$(PYTHON) $(TEST_DIR)/test_models/test_amenity.py
	@echo "$(GREEN)✅ Model tests complete!$(NC)"

# Test only the facade functionality
# Useful when working on the service layer
test-facade:
	@echo "$(YELLOW)🧪 Testing facade functionality...$(NC)"
	$(PYTHON) $(TEST_DIR)/test_models/test_facade.py
	@echo "$(GREEN)✅ Facade tests complete!$(NC)"

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

# Start the Flask development server
# The application will be available at http://localhost:5000
# API documentation will be at http://localhost:5000/api/v1/
run:
	@echo "$(YELLOW)🚀 Starting Flask application...$(NC)"
	@echo "$(BLUE)Application will be available at: http://localhost:5000$(NC)"
	@echo "$(BLUE)API documentation at: http://localhost:5000/api/v1/$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop the server$(NC)"
	@echo ""
	$(PYTHON) run.py

# Show project status and useful information
# Helpful for debugging and understanding the current state
status:
	@echo "$(BLUE)📊 HBnB Project Status$(NC)"
	@echo "======================"
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Current directory: $(shell pwd)"
	@echo "Project structure:"
	@find . -name "*.py" -not -path "./venv/*" -not -path "./__pycache__/*" | head -15
	@echo ""
	@echo "Dependencies status:"
	@$(PYTHON) -c "import flask; print('✅ Flask installed')" 2>/dev/null || echo "❌ Flask not installed"
	@$(PYTHON) -c "import flask_restx; print('✅ Flask-RESTx installed')" 2>/dev/null || echo "❌ Flask-RESTx not installed"

# =============================================================================
# CLEANUP COMMANDS
# =============================================================================

# Clean up temporary files and caches
# Run this before committing code to keep the repository clean
clean:
	@echo "$(YELLOW)🧹 Cleaning up temporary files...$(NC)"
	@echo "Removing Python cache files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

# =============================================================================
# SPECIAL TARGETS
# =============================================================================

# .PHONY tells make that these are command names, not file names
# This prevents conflicts if files with these names exist
.PHONY: help install setup venv dev-setup test test-quick test-models test-facade run status clean

# =============================================================================
# TROUBLESHOOTING GUIDE
# =============================================================================
#
# Common Issues and Solutions:
#
# 1. "make: command not found"
#    - On Windows: Install make or use WSL (Windows Subsystem for Linux)
#    - On Mac: Install Xcode command line tools: xcode-select --install
#    - Alternative: Run commands manually (see individual targets above)
#
# 2. "python3: command not found"
#    - Install Python 3.6 or higher from python.org
#    - On some systems, try 'python' instead of 'python3'
#    - Update the PYTHON variable at the top of this file if needed
#
# 3. "Permission denied" errors
#    - Try: sudo make install
#    - Or use virtual environment: make venv, activate it, then make install
#
# 4. Tests failing
#    - Check that all model files exist in app/models/
#    - Verify that __init__.py files exist in all directories
#    - Run make status to check project structure
#
# 5. Flask app won't start
#    - Check that run.py exists in project root
#    - Verify Flask is installed: python3 -c "import flask"
#    - Check for syntax errors: python3 -m py_compile run.py
#
# =============================================================================