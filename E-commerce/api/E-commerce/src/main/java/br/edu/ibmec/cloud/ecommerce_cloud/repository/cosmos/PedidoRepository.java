package br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Pedido;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PedidoRepository extends CosmosRepository<Pedido, String> {
}
