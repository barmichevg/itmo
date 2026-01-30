package ru.itmo.lab4.api;

import java.time.Instant;
import java.util.List;

public record ApiError(
        Instant timestamp,
        int status,
        String error,
        String path,
        String message,
        List<String> errors
) {}
