package fra.uas.intellimatch.intellimatch.repository;

import fra.uas.intellimatch.intellimatch.model.Address;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AddressRepository extends JpaRepository<Address, Integer> {

}

