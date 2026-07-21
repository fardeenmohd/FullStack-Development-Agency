package com.b2b.trade.service;

import com.b2b.trade.dto.ProductRequest;
import com.b2b.trade.entity.Product;
import com.b2b.trade.entity.User;
import com.b2b.trade.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ComputeClientService computeClientService;

    @Transactional
    public Product createProduct(ProductRequest request, User exporter) {
        Product product = new Product();
        product.setExporter(exporter);
        product.setName(request.getName());
        product.setHsCode(request.getHsCode());
        product.setDescription(request.getDescription());
        product.setTargetRegions(request.getTargetRegions());

        Product savedProduct = productRepository.save(product);

        // Trigger AI Lead Hunter asynchronously via WebClient
        computeClientService.triggerHuntLeads(savedProduct.getId())
                .subscribe(null, err -> System.err.println("Failed to trigger lead hunt: " + err.getMessage()));

        return savedProduct;
    }
}