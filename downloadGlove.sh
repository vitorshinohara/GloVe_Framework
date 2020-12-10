echo 'Creating Glove folder'
mkdir -p Embedding
echo 'Downloading Glove Embeddings'
cd Embedding/
wget http://nlp.stanford.edu/data/glove.6B.zip -q --show-progress -O glove.zip
unzip glove.zip
