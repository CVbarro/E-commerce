package br.edu.ibmec.cloud.ecommerce_cloud.configuration;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;

@Getter
@Setter
@ConfigurationProperties(prefix = "azure.cosmos")
public class CosmosProperties {

    private String uri;

    private String key;

    private String database;

    private boolean queryMetricsEnabled;

    private boolean responseDiagnosticsEnabled;

}
