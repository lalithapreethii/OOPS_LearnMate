package com.knowwhereyoulack.controller;

import com.knowwhereyoulack.model.Note;
import com.knowwhereyoulack.service.NoteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/notes")
@CrossOrigin(origins = "http://localhost:5173")
public class NotesController {
    
    @Autowired
    private NoteService noteService;
    
    // Get all notes for user
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Note>> getUserNotes(@PathVariable Long userId) {
        return ResponseEntity.ok(noteService.getUserNotes(userId));
    }
    
    // Get notes by subject
    @GetMapping("/user/{userId}/subject/{subject}")
    public ResponseEntity<List<Note>> getNotesBySubject(
            @PathVariable Long userId, 
            @PathVariable String subject) {
        return ResponseEntity.ok(noteService.getNotesBySubject(userId, subject));
    }
    
    // Create new note
    @PostMapping
    public ResponseEntity<Note> createNote(@RequestBody Note note) {
        Note created = noteService.createNote(note);
        return ResponseEntity.ok(created);
    }
    
    // Update note
    @PutMapping("/{id}")
    public ResponseEntity<Note> updateNote(@PathVariable Long id, @RequestBody Note note) {
        Note updated = noteService.updateNote(id, note);
        if (updated != null) {
            return ResponseEntity.ok(updated);
        }
        return ResponseEntity.notFound().build();
    }
    
    // Delete note
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteNote(@PathVariable Long id) {
        noteService.deleteNote(id);
        return ResponseEntity.ok().build();
    }
}
