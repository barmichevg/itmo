package ru.itmo.lab4.api;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.itmo.lab4.hit.Hit;
import ru.itmo.lab4.hit.HitService;

import java.security.Principal;
import java.util.List;

@RestController
@RequestMapping("/api/hits")
public class HitController {

    private final HitService hitService;

    public HitController(HitService hitService) {
        this.hitService = hitService;
    }

    @GetMapping
    public List<HitResponse> list(Principal principal) {
        return hitService.listForUser(principal.getName()).stream()
                .map(HitController::toDto)
                .toList();
    }

    @PostMapping
    public HitResponse create(@RequestBody @Valid HitRequest req, Principal principal) {
        Hit hit = hitService.create(principal.getName(), req);
        return toDto(hit);
    }

    @DeleteMapping
    public ResponseEntity<Void> clear(Principal principal) {
        hitService.clearForUser(principal.getName());
        return ResponseEntity.noContent().build();
    }

    private static HitResponse toDto(Hit h) {
        return new HitResponse(
                h.getId(),
                h.getX(),
                h.getY(),
                h.getR(),
                h.isHit(),
                h.getCreatedAt(),
                h.getScriptMicros()
        );
    }
}
