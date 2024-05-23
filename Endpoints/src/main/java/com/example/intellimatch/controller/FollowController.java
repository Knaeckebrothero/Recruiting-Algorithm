package com.example.intellimatch.controller;

import com.example.intellimatch.model.Follow;
import com.example.intellimatch.service.FollowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/follows")
public class FollowController {

    private final FollowService followService;

    @Autowired
    public FollowController(FollowService followService) {
        this.followService = followService;
    }

    @GetMapping
    public ResponseEntity<List<Follow>> getAllFollows() {
        List<Follow> follows = followService.getAllFollows();
        return ResponseEntity.ok(follows);
    }

    @GetMapping("/{followId}")
    public ResponseEntity<Follow> getFollowById(@PathVariable Integer followId) {
        Optional<Follow> follow = followService.getFollowById(followId);
        return follow.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Follow> createFollow(@RequestBody Follow follow) {
        followService.saveFollow(follow);
        return new ResponseEntity<>(follow, HttpStatus.CREATED);
    }

    @PutMapping("/{followId}")
    public ResponseEntity<Follow> updateFollow(@PathVariable Integer followId, @RequestBody Follow updatedFollow) {
        Optional<Follow> existingFollow = followService.getFollowById(followId);
        if (existingFollow.isPresent()) {
            updatedFollow.setId(followId);
            followService.saveFollow(updatedFollow);
            return ResponseEntity.ok(updatedFollow);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{followId}")
    public ResponseEntity<Void> deleteFollow(@PathVariable Integer followId) {
        Optional<Follow> follow = followService.getFollowById(followId);
        if (follow.isPresent()) {
            followService.deleteFollow(followId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

