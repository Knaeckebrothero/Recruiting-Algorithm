package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.model.Follow;
import fra.uas.intellimatch.intellimatch.repository.FollowRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class FollowService {

    private final FollowRepository followRepository;

    @Autowired
    public FollowService(FollowRepository followRepository) {
        this.followRepository = followRepository;
    }

    public List<Follow> getAllFollows() {
        return followRepository.findAll();
    }

    public Optional<Follow> getFollowById(Integer followId) {
        return followRepository.findById(followId);
    }

    public void saveFollow(Follow follow) {
        followRepository.save(follow);
    }

    public void deleteFollow(Integer followId) {
        followRepository.deleteById(followId);
    }
}
