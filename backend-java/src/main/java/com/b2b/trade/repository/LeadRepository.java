package com.b2b.trade.repository;

import com.b2b.trade.entity.Lead;
import com.b2b.trade.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.UUID;

public interface LeadRepository extends JpaRepository<Lead, UUID> {
    List<Lead> findByExporter(User exporter);
    long countByExporter(User exporter);
}