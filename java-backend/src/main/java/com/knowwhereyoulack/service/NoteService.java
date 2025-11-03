package com.knowwhereyoulack.service;

import com.knowwhereyoulack.model.Note;
import com.knowwhereyoulack.repository.NoteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class NoteService {
    
    @Autowired
    private NoteRepository noteRepository;
    
    public List<Note> getUserNotes(Long userId) {
        return noteRepository.findByUserIdOrderByUpdatedAtDesc(userId);
    }
    
    public List<Note> getNotesBySubject(Long userId, String subject) {
        return noteRepository.findByUserIdAndSubject(userId, subject);
    }
    
    public Note createNote(Note note) {
        return noteRepository.save(note);
    }
    
    public Note updateNote(Long id, Note updatedNote) {
        Optional<Note> existing = noteRepository.findById(id);
        if (existing.isPresent()) {
            Note note = existing.get();
            note.setTitle(updatedNote.getTitle());
            note.setContent(updatedNote.getContent());
            note.setSubject(updatedNote.getSubject());
            return noteRepository.save(note);
        }
        return null;
    }
    
    public void deleteNote(Long id) {
        noteRepository.deleteById(id);
    }
}
