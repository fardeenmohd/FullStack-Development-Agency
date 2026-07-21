package com.b2b.trade.service;

import com.b2b.trade.dto.ProductRequest;
import com.b2b.trade.entity.Product;
import com.b2b.trade.entity.User;
import com.b2b.trade.repository.ProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Mono;
import java.util.List;
import java.util.UUID;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @Mock
    private ComputeClientService computeClientService;

    @InjectMocks
    private ProductService productService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testCreateProduct_Success() {
        User exporter = new User();
        exporter.setId(UUID.randomUUID());

        ProductRequest request = new ProductRequest();
        request.setName("Organic Basmati Rice");
        request.setHsCode("10063020");
        request.setDescription("Premium long-grain organic Basmati rice from Punjab.");
        request.setTargetRegions(List.of("OM", "EU"));

        Product savedProduct = new Product();
        savedProduct.setId(UUID.randomUUID());
        savedProduct.setExporter(exporter);
        savedProduct.setName(request.getName());
        savedProduct.setHsCode(request.getHsCode());
        savedProduct.setDescription(request.getDescription());
        savedProduct.setTargetRegions(request.getTargetRegions());

        when(productRepository.save(any(Product.class))).thenReturn(savedProduct);
        when(computeClientService.triggerHuntLeads(any(UUID.class))).thenReturn(Mono.empty());

        Product result = productService.createProduct(request, exporter);

        assertNotNull(result);
        assertEquals("Organic Basmati Rice", result.getName());
        verify(productRepository, times(1)).save(any(Product.class));
        verify(computeClientService, times(1)).triggerHuntLeads(any(UUID.class));
    }
}