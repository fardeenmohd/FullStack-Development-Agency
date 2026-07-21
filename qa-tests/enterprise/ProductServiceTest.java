import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class ProductServiceTest {
    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testGetProductsByExporterId() {
        UUID exporterId = UUID.randomUUID();
        List<Product> products = List.of(new Product(), new Product());
        when(productRepository.findByExporterId(exporterId)).thenReturn(products);

        List<Product> result = productService.getProductsByExporterId(exporterId);

        assertEquals(products, result);
    }

    @Test
    public void testSaveProduct() {
        Product product = new Product();
        when(productRepository.save(any(Product.class))).thenReturn(product);

        Product savedProduct = productService.saveProduct(product);

        assertEquals(product, savedProduct);
    }
}
