package fra.uas.intellimatch.intellimatch.service;

import fra.uas.intellimatch.intellimatch.model.Address;
import fra.uas.intellimatch.intellimatch.repository.AddressRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AddressService {

    private final AddressRepository addressRepository;

    @Autowired
    public AddressService(AddressRepository addressRepository) {
        this.addressRepository = addressRepository;
    }

    public List<Address> getAllAddresses() {
        return addressRepository.findAll();
    }

    public Optional<Address> getAddressById(Integer addressId) {
        return addressRepository.findById(addressId);
    }

    public void saveAddress(Address address) {
        addressRepository.save(address);
    }

    public void deleteAddress(Integer addressId) {
        addressRepository.deleteById(addressId);
    }
}


