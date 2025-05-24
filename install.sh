text='                  _       _   _       _              
                 | |     | \ | |     | |             
    __      _____| |__   |  \| |_   _| |_ ___  _ __  
    \ \ /\ / / _ \ '\''_ \  | . ` \ \ / / __/ _ \| '\''_ \ 
     \ V  V /  __/ |_) | | |\  |\ V /| || (_) | |_) |
      \_/\_/ \___|_.__/  \_| \_/ \_/  \__\___/| .__/ 
                                              | |    
                                              |_|    '

BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}${text}${NC}"

REPO_URL="https://github.com/ArnauCosta/web-nvtop.git"

git clone "$REPO_URL"

REPO_NAME=$(basename "$REPO_URL" .git)

cd "$REPO_NAME" || { echo "Failed to enter repo directory"; exit 1; }

chmod +x run.sh

./run.sh
