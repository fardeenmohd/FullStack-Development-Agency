package com.b2b.trade.service;

import com.b2b.trade.config.CustomUserDetails;
import com.b2b.trade.config.JwtUtils;
import com.b2b.trade.dto.LoginRequest;
import com.b2b.trade.dto.LoginResponse;
import com.b2b.trade.dto.RegisterRequest;
import com.b2b.trade.dto.RegisterResponse;
import com.b2b.trade.entity.Role;
import com.b2b.trade.entity.User;
import com.b2b.trade.exception.CustomException;
import com.b2b.trade.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.Map;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtils jwtUtils;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Transactional
    public RegisterResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new CustomException("Email is already registered", HttpStatus.BAD_REQUEST);
        }

        // Validation: Import Export Code required if role is EXPORTER and country is 'India'
        if (request.getRole() == Role.EXPORTER && "India".equalsIgnoreCase(request.getCountry())) {
            if (request.getIecCode() == null || request.getIecCode().trim().isEmpty()) {
                throw new CustomException("IEC Code is required for Indian Exporters", HttpStatus.BAD_REQUEST);
            }
        }

        User user = new User();
        user.setEmail(request.getEmail());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setCompanyName(request.getCompanyName());
        user.setRole(request.getRole());
        user.setCountry(request.getCountry());
        user.setIecCode(request.getIecCode());

        User savedUser = userRepository.save(user);

        return new RegisterResponse(
                savedUser.getId(),
                savedUser.getEmail(),
                savedUser.getCompanyName(),
                savedUser.getRole(),
                savedUser.getCountry(),
                savedUser.getIecCode(),
                savedUser.getCreatedAt()
        );
    }

    public LoginResponse login(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );

        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
        User user = userDetails.getUser();

        String token = jwtUtils.generateToken(userDetails, Map.of(
                "role", user.getRole().name(),
                "companyName", user.getCompanyName()
        ));

        return new LoginResponse(token, user.getEmail(), user.getCompanyName(), user.getRole());
    }
}