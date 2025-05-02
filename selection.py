import sqlite3
from typing import List
from PIL import Image
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import CLIPModel, CLIPProcessor

class SemanticRecommender:
    def __init__(self, db_path="products.db", model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.db_path = db_path
        self.product_embeddings = {}
        self.all_products = []
        self.all_embeddings = None
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32",use_fast=False)
        self.image_embeddings = []
        self.image_products = []
        self._load_embeddings()

    def _fetch_all_products(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, category, image_path, link FROM products")
        results = cursor.fetchall()
        conn.close()
        return results

    def _load_embeddings(self):
        products = self._fetch_all_products()

        text_category_map = {}
        image_category_map = {}

        for prod in products:
            cat = prod[3] or "Uncategorized"
            text_category_map.setdefault(cat, []).append(prod)
            image_category_map.setdefault(cat, []).append(prod)

        for cat, plist in text_category_map.items():
            descriptions = [p[2] for p in plist]
            embeddings = self.model.encode(descriptions, convert_to_tensor=True)
            self.product_embeddings[cat] = (plist, embeddings)

        self.all_products = products
        self.all_embeddings = self.model.encode([p[2] for p in products], convert_to_tensor=True)

        self.image_embeddings = {}
        self.all_image_products = []
        all_image_embeds = []

        for cat, plist in image_category_map.items():
            emb_list = []
            valid_products = []
            for prod in plist:
                image_path = prod[4]
                try:
                    image = Image.open(image_path).convert("RGB")
                    inputs = self.clip_processor(images=image, return_tensors="pt")
                    with torch.no_grad():
                        image_emb = self.clip_model.get_image_features(**inputs).squeeze()
                        image_emb = image_emb / image_emb.norm()
                    emb_list.append(image_emb)
                    valid_products.append(prod)
                    self.all_image_products.append(prod)
                    all_image_embeds.append(image_emb)
                except Exception as e:
                    print(f" Image loading fail：{image_path}，due to：{e}")
            if valid_products:
                self.image_embeddings[cat] = (valid_products, torch.stack(emb_list))

        self.all_image_embeddings = torch.stack(all_image_embeds) if all_image_embeds else None

    def _top_k_from_embedding(self, query_embedding, embeddings, products, top_k):
        cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(top_k, len(products)))

        top_items = []
        for idx in top_results.indices:
            pid, name, description,_, image_path, link = products[idx]
            top_items.append({
                "name": name,
                "description": description,
                "image_path": image_path,
                "link": link
            })
        return top_items

    def query(self, semantic_query: str, category: List[str] = None, top_k=5):
        query_embedding = self.model.encode(semantic_query, convert_to_tensor=True)

        if category:
            selected_products = []
            selected_embeddings = []

            for cat in category:
                if cat in self.product_embeddings:
                    products, embeddings = self.product_embeddings[cat]
                    selected_products.extend(products)
                    selected_embeddings.append(embeddings)

            if not selected_products:
                return []

            embeddings = torch.cat(selected_embeddings, dim=0)
            products = selected_products
        else:

            embeddings = self.all_embeddings
            products = self.all_products

        return self._top_k_from_embedding(query_embedding, embeddings, products, top_k)

    def query_by_image(self, image_path:str, category: List[str] = None, top_k=5):

        image = Image.open(image_path).convert("RGB")
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            query_embedding = self.clip_model.get_image_features(**inputs).squeeze()
            query_embedding = query_embedding / query_embedding.norm()

        if not self.image_embeddings:
            return []

        if category:
            selected_products = []
            selected_embeddings = []

            for cat in category:
                if cat in self.image_embeddings:
                    plist, embeds = self.image_embeddings[cat]
                    selected_products.extend(plist)
                    selected_embeddings.append(embeds)

            if not selected_products:
                return []

            embeddings = torch.cat(selected_embeddings, dim=0)
            products = selected_products
        else:
            embeddings = self.all_image_embeddings
            products = self.all_image_products

        return self._top_k_from_embedding(query_embedding, embeddings, products, top_k)

if __name__ == "__main__":
    recommender = SemanticRecommender()

    result = recommender.query("cold refreshing sweet drink", category=["Beverages", "Food","Electronics"])
    for item in result:
        print(f"- {item['name']} ")

    test_image = Image.open("img_1.png")

    result = recommender.query_by_image(test_image, category=["Beverages", "Food","Electronics"])

    print("\n Top Image-Based Recommendations:")
    print(type(result[0]))
    print(result[0])