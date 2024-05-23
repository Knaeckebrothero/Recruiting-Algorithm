package fra.uas.intellimatch.intellimatch.repository;

import fra.uas.intellimatch.intellimatch.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

}

