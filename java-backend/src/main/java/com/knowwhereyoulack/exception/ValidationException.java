package com.knowwhereyoulack.exception;

public class ValidationException extends RuntimeException {
    public ValidationException(String msg) { 
        super(msg); 
    }
}