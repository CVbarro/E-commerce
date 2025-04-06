package br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos;



import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends JpaRepository<Produto, Integer> {
}
