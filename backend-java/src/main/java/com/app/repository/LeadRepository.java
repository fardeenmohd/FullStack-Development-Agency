package com.app.repository;

import java.util.UUID;

import com.app.model.Lead;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LeadRepository extends JpaRepository<Lead, UUID> {
}
