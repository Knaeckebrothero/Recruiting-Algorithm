package fra.uas.intellimatch.intellimatch.repository;

import fra.uas.intellimatch.intellimatch.model.Post;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PostRepository extends JpaRepository<Post, Integer> {

}

