package br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Pedido;
import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface PedidoRepository extends JpaRepository<Pedido, String> {
}

