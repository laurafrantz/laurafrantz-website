#!/bin/bash

# Script to add cover = "" field to all post index.md files that don't have it
# Usage: bash add-cover-field.sh

POSTS_DIR="content/posts"
UPDATED_COUNT=0

echo "Scanning posts in $POSTS_DIR for missing cover field..."
echo ""

for post_dir in "$POSTS_DIR"/*/; do
    index_file="${post_dir}index.md"
    
    if [ -f "$index_file" ]; then
        # Check if the file already has a cover field
        if ! grep -q "^cover = " "$index_file"; then
            post_name=$(basename "$post_dir")
            echo "Adding cover field to: $post_name"
            
            # Add cover = "" after the frontmatter opening (after +++), before other fields
            # We'll insert it right before the first tag/field line after +++
            sed -i.bak '/^+++$/a\
cover = ""' "$index_file"
            
            # Clean up backup file
            rm "${index_file}.bak"
            
            UPDATED_COUNT=$((UPDATED_COUNT + 1))
        fi
    fi
done

echo ""
echo "✓ Complete! Updated $UPDATED_COUNT posts with the cover field."
