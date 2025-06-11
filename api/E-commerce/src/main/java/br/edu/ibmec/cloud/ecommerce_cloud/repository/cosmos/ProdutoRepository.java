package br.edu.ibmec.cloud.ecommerce_cloud.repository.cosmos;

import br.edu.ibmec.cloud.ecommerce_cloud.model.Produto;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ProdutoRepository extends CosmosRepository<Produto, String> {
    Optional<List<Produto>> findByProdutoNomeContains(String produtoNome);
}
