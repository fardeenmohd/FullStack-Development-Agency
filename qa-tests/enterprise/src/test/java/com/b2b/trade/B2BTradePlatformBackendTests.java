package com.b2b.trade;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.util.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

class User {
    private UUID id;
    private String email;
    private String passwordHash;
    private String companyName;
    private String role;
    private String country;
    private String iecCode;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
}

class Product {
    private UUID id;
    private UUID exporterId;
    private String name;
    private String hsCode;
    private String description;
    private List<String> targetRegions;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getExporterId() { return exporterId; }
    public void setExporterId(UUID exporterId) { this.exporterId = exporterId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getHsCode() { return hsCode; }
    public void setHsCode(String hsCode) { this.hsCode = hsCode; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public List<String> getTargetRegions() { return targetRegions; }
    public void setTargetRegions(List<String> targetRegions) { this.targetRegions = targetRegions; }
}

class Lead {
    private UUID id;
    private UUID exporterId;
    private String companyName;
    private String country;
    private String contactEmail;
    private BigDecimal confidenceScore;
    private String sourceUrl;
    private String status;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getExporterId() { return exporterId; }
    public void setExporterId(UUID exporterId) { this.exporterId = exporterId; }
    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public BigDecimal getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(BigDecimal confidenceScore) { this.confidenceScore = confidenceScore; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}

class Transaction {
    private UUID id;
    private UUID leadId;
    private UUID exporterId;
    private BigDecimal contractValue;
    private String currency;
    private String status;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getLeadId() { return leadId; }
    public void setLeadId(UUID leadId) { this.leadId = leadId; }
    public UUID getExporterId() { return exporterId; }
    public void setExporterId(UUID exporterId) { this.exporterId = exporterId; }
    public BigDecimal getContractValue() { return contractValue; }
    public void setContractValue(BigDecimal contractValue) { this.contractValue = contractValue; }
    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}

class RegisterRequest {
    public String email;
    public String password;
    public String companyName;
    public String role;
    public String country;
    public String iecCode;
}

class LoginRequest {
    public String email;
    public String password;
}

class AuthResponse {
    public String token;
    public String email;
    public String role;
}

class DashboardMetrics {
    public long activeLeadsCount;
    public long pendingTransactionsCount;
    public BigDecimal totalContractValue;
}

interface AuthService {
    User register(RegisterRequest request);
    AuthResponse login(LoginRequest request);
}

interface ProductService {
    Product createProduct(UUID exporterId, Product product);
}

interface LeadService {
    List<Lead> getLeadsForExporter(UUID exporterId);
}

interface TransactionService {
    Transaction initiateTransaction(UUID exporterId, UUID leadId, BigDecimal contractValue, String currency);
}

interface DashboardService {
    DashboardMetrics getMetrics(UUID exporterId);
}

class AuthController {
    private final AuthService authService;
    public AuthController(AuthService authService) { this.authService = authService; }
    public ResponseEntity<?> register(RegisterRequest request) {
        try {
            User user = authService.register(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(user);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } 
    }
    public ResponseEntity<?> login(LoginRequest request) {
        try {
            AuthResponse response = authService.login(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(e.getMessage());
        }
    }
}

class ProductController {
    private final ProductService productService;
    public ProductController(ProductService productService) { this.productService = productService; }
    public ResponseEntity<?> createProduct(UUID exporterId, Product product) {
        try {
            Product created = productService.createProduct(exporterId, product);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}

class LeadController {
    private final LeadService leadService;
    public LeadController(LeadService leadService) { this.leadService = leadService; }
    public ResponseEntity<?> getLeads(UUID exporterId) {
        try {
            List<Lead> leads = leadService.getLeadsForExporter(exporterId);
            return ResponseEntity.ok(leads);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}

class TransactionController {
    private final TransactionService transactionService;
    public TransactionController(TransactionService transactionService) { this.transactionService = transactionService; }
    public ResponseEntity<?> initiateTransaction(UUID exporterId, UUID leadId, BigDecimal contractValue, String currency) {
        try {
            Transaction tx = transactionService.initiateTransaction(exporterId, leadId, contractValue, currency);
            return ResponseEntity.status(HttpStatus.CREATED).body(tx);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}

class DashboardController {
    private final DashboardService dashboardService;
    public DashboardController(DashboardService dashboardService) { this.dashboardService = dashboardService; }
    public ResponseEntity<?> getMetrics(UUID exporterId) {
        try {
            DashboardMetrics metrics = dashboardService.getMetrics(exporterId);
            return ResponseEntity.ok(metrics);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}

@ExtendWith(MockitoExtension.class)
public class B2BTradePlatformBackendTests {

    @Mock private AuthService authService;
    @Mock private ProductService productService;
    @Mock private LeadService leadService;
    @Mock private TransactionService transactionService;
    @Mock private DashboardService dashboardService;

    @InjectMocks private AuthController authController;
    @InjectMocks private ProductController productController;
    @InjectMocks private LeadController leadController;
    @InjectMocks private TransactionController transactionController;
    @InjectMocks private DashboardController dashboardController;

    private UUID exporterId;
    private UUID leadId;

    @BeforeEach
    void setUp() {
        exporterId = UUID.randomUUID();
        leadId = UUID.randomUUID();
    }

    @Test
    void testRegister_Success() {
        RegisterRequest req = new RegisterRequest();
        req.email = "exporter@india.com";
        req.password = "securePass123";
        req.companyName = "India Exports Ltd";
        req.role = "EXPORTER";
        req.country = "India";
        req.iecCode = "IEC1234567";

        User mockUser = new User();
        mockUser.setId(exporterId);
        mockUser.setEmail(req.email);
        mockUser.setRole(req.role);

        when(authService.register(any(RegisterRequest.class))).thenReturn(mockUser);

        ResponseEntity<?> response = authController.register(req);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(mockUser, response.getBody());
    }

    @Test
    void testLogin_Success() {
        LoginRequest req = new LoginRequest();
        req.email = "exporter@india.com";
        req.password = "securePass123";

        AuthResponse mockResponse = new AuthResponse();
        mockResponse.token = "mock-jwt-token";
        mockResponse.email = req.email;
        mockResponse.role = "EXPORTER";

        when(authService.login(any(LoginRequest.class))).thenReturn(mockResponse);

        ResponseEntity<?> response = authController.login(req);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(mockResponse, response.getBody());
    }

    @Test
    void testCreateProduct_Success() {
        Product product = new Product();
        product.setName("Basmati Rice");
        product.setHsCode("10063020");
        product.setDescription("Premium long-grain aromatic Basmati rice.");
        product.setTargetRegions(Arrays.asList("OM", "EU"));

        Product createdProduct = new Product();
        createdProduct.setId(UUID.randomUUID());
        createdProduct.setExporterId(exporterId);
        createdProduct.setName(product.getName());
        createdProduct.setHsCode(product.getHsCode());

        when(productService.createProduct(eq(exporterId), any(Product.class))).thenReturn(createdProduct);

        ResponseEntity<?> response = productController.createProduct(exporterId, product);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(createdProduct, response.getBody());
    }

    @Test
    void testGetLeads_Success() {
        Lead lead = new Lead();
        lead.setId(leadId);
        lead.setExporterId(exporterId);
        lead.setCompanyName("Oman Food Importers");
        lead.setCountry("Oman");
        lead.setConfidenceScore(new BigDecimal("92.50"));
        lead.setStatus("NEW");

        List<Lead> mockLeads = Collections.singletonList(lead);

        when(leadService.getLeadsForExporter(exporterId)).thenReturn(mockLeads);

        ResponseEntity<?> response = leadController.getLeads(exporterId);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(mockLeads, response.getBody());
    }

    @Test
    void testInitiateTransaction_Success() {
        BigDecimal contractValue = new BigDecimal("50000.00");
        String currency = "USD";

        Transaction mockTx = new Transaction();
        mockTx.setId(UUID.randomUUID());
        mockTx.setLeadId(leadId);
        mockTx.setExporterId(exporterId);
        mockTx.setContractValue(contractValue);
        mockTx.setCurrency(currency);
        mockTx.setStatus("INITIATED");

        when(transactionService.initiateTransaction(eq(exporterId), eq(leadId), eq(contractValue), eq(currency)))
                .thenReturn(mockTx);

        ResponseEntity<?> response = transactionController.initiateTransaction(exporterId, leadId, contractValue, currency);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(mockTx, response.getBody());
    }

    @Test
    void testGetDashboardMetrics_Success() {
        DashboardMetrics mockMetrics = new DashboardMetrics();
        mockMetrics.activeLeadsCount = 12;
        mockMetrics.pendingTransactionsCount = 3;
        mockMetrics.totalContractValue = new BigDecimal("150000.00");

        when(dashboardService.getMetrics(exporterId)).thenReturn(mockMetrics);

        ResponseEntity<?> response = dashboardController.getMetrics(exporterId);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(mockMetrics, response.getBody());
    }
}
