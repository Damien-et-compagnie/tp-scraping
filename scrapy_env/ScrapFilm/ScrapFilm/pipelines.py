# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import json

class ScrapfilmPipeline:
    def process_item(self, item, spider):
        # Processes and writes a scraped item to a CSV file.

        # This method adapts the input item using an ItemAdapter and writes
        # specific fields of the item to a CSV file using a CSV writer. It
        # also prints a confirmation message indicating the item has been
        # saved.

        # Parameters:
        # item (dict): The scraped item to be processed.
        # spider (scrapy.Spider): The spider instance that scraped the item.
        
        # Returns:
        # dict: The processed item.
        adapter = ItemAdapter(item)

        self.writer.writerow([
            adapter.get("titre"),
            adapter.get("genres"),
            adapter.get("realisateurs"),
            adapter.get("note_presse"),
            adapter.get("note_spectateurs")
        ])

        if not hasattr(self, 'json') or not isinstance(self.json, dict):
            self.json = {}
            self.json["films"] = {}

        json_data = {
            adapter.get("titre") : {
                "genres": adapter.get("genres"),
                "realisateurs": adapter.get("realisateurs"),
                "note_presse": adapter.get("note_presse"),
                "note_spectateurs": adapter.get("note_spectateurs")
            }
        }

        self.json["films"].update(json_data)

        return item
    
    def open_spider(self, spider):
        # Initializes resources required for writing items to a CSV file when the spider opens.

        # This method opens a CSV file for writing and initializes a CSV writer object. 
        # It also writes the header row to the file.

        # Parameters:
        # spider (scrapy.Spider): The spider instance that is opening.
        
        print("Pipeline opened")
        self.file = open("../data/final_dataset.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        self.file_json = open("../data/final_dataset.json", "w", encoding="utf-8")

        self.writer.writerow(["titre", "genres", "realisateurs", "note_presse", "note_spectateurs"])

    def close_spider(self, spider):
        # Finalizes resources and closes the CSV file when the spider closes.

        # This method is responsible for closing the CSV file opened during the spider's operation.
        # It ensures that all resources are properly released and prints a closing confirmation message.

        # Parameters:
        # spider (scrapy.Spider): The spider instance that is closing.
        print("Pipeline closed")
        self.file.close()
        json.dump(self.json, self.file_json, ensure_ascii=False, indent=4)
        
        self.file_json.close()
