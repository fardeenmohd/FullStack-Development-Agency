package com.b2b.trade.controller;

import com.b2b.trade.dto.RegisterRequest;
import com.b2b.trade.entity.Role;
import com.b2b.trade.repository.UserRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

@SpringBootTest
@AutoConfigureMockMvc
public class AuthControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @BeforeEach
    public void cleanDatabase() {
        userRepository.deleteAll();
    }

    @Test
    public void testRegister_Success() throws Exception {
        RegisterRequest request = new RegisterRequest();
        request.setEmail("exporter@india.com");
        request.setPassword("SecurePassword123!");
        request.setCompanyName("Bharat Exports Ltd");
        request.setRole(Role.EXPORTER);
        request.setCountry("India");
        request.setIecCode("IEC1234567");

        mockMvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email").value("exporter@india.com"))
                .andExpect(jsonPath("$.companyName").value("Bharat Exports Ltd"));
    }

    @Test
    public void testRegister_MissingIecCodeForIndianExporter_ThrowsBadRequest() throws Exception {
        RegisterRequest request = new RegisterRequest();
        request.setEmail("exporter2@india.com");
        request.setPassword("SecurePassword123!");
        request.setCompanyName("Bharat Exports Ltd");
        request.setRole(Role.EXPORTER);
        request.setCountry("India");
        request.setIecCode(null); // Missing IEC code

        mockMvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("IEC Code is required for Indian Exporters\n"));
    }
}