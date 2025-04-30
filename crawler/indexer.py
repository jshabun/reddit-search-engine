import json
import os
import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths

def parse_json(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

def create_index(data, index_dir):
    lucene.initVM()
    index_path = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(index_path, config)

    for item in data:
        doc = Document()
        doc.add(StringField("username", item.get("username", ""), Field.Store.YES))
        doc.add(StringField("timestamp", item.get("timestamp", ""), Field.Store.YES))
        doc.add(TextField("body", item.get("body", ""), Field.Store.YES))
        # Add other fields as needed
        writer.addDocument(doc)
    
    writer.close()

if __name__ == "__main__":
    json_file_path = '/mnt/data/worldnews_1_sampleData.jsonl'
    index_directory = '/mnt/data/index'
    
    if not os.path.exists(index_directory):
        os.makedirs(index_directory)
    
    data = parse_json(json_file_path)
    create_index(data, index_directory)
    print("Indexing completed.")