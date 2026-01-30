package ru.itmo.lab4.common;

import java.util.List;

public class ValidationException extends RuntimeException {
    private final List<String> messages;

    public ValidationException(List<String> messages) {
        super(String.join("; ", messages));
        this.messages = messages;
    }

    public List<String> getMessages() {
        return messages;
    }
}
