package ru.itmo.lab4.api;

import java.math.BigDecimal;
import java.time.Instant;

public record HitResponse(
        Long id,
        BigDecimal x,
        BigDecimal y,
        BigDecimal r,
        boolean hit,
        Instant createdAt,
        long scriptMicros
) {}
