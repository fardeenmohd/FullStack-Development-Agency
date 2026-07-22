class ProductAnalytics:
    def __init__(self, total_sales, average_contract_value, top_selling_products, areas_for_improvement):
        self.total_sales = total_sales
        self.average_contract_value = average_contract_value
        self.top_selling_products = top_selling_products
        self.areas_for_improvement = areas_for_improvement

    def __repr__(self):
        return f"ProductAnalytics(total_sales={self.total_sales}, average_contract_value={self.average_contract_value}, top_selling_products={self.top_selling_products}, areas_for_improvement={self.areas_for_improvement})"
