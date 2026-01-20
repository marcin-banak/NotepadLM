# Makefile for PDFLaTeX compilation

# Output file name (without extension)
TARGET = thesis

# Source file
SOURCE = $(TARGET).tex

# Output directory
OUTDIR = build

# Compiler
PDFLATEX = pdflatex

# Flags for pdflatex
PDFLATEX_FLAGS = -interaction=nonstopmode -output-directory=$(OUTDIR)

# Default target - compile and clean
.PHONY: all
all: $(TARGET).pdf clean

# Build the PDF
$(TARGET).pdf: $(SOURCE)
	@mkdir -p $(OUTDIR)
	$(PDFLATEX) $(PDFLATEX_FLAGS) $(SOURCE)
	$(PDFLATEX) $(PDFLATEX_FLAGS) $(SOURCE)
	@mv $(OUTDIR)/$(TARGET).pdf .

# Clean auxiliary files (but keep the PDF)
.PHONY: clean
clean:
	@rm -rf $(OUTDIR)
	@rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.fls *.fdb_latexmk

# Deep clean - remove everything including PDFs
.PHONY: distclean
distclean: clean
	@rm -f $(TARGET).pdf

# Rebuild from scratch
.PHONY: rebuild
rebuild: distclean all

# Watch mode - compile on file changes (requires fswatch)
.PHONY: watch
watch:
	fswatch -o $(SOURCE) | xargs -n1 -I{} make all

# Help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make              - Compile PDF and clean auxiliary files"
	@echo "  make clean        - Remove auxiliary files"
	@echo "  make distclean    - Remove all generated files including PDF"
	@echo "  make rebuild      - Clean and recompile from scratch"
	@echo "  make watch       - Watch file and recompile on changes"
	@echo "  make help        - Show this help message"
