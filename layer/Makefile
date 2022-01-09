build-ImageGenerateLayer:
	mkdir -p "$(ARTIFACTS_DIR)/python"
	python -m pip install htmlwebshot -t "$(ARTIFACTS_DIR)/python"
	wget -O "$(ARTIFACTS_DIR)/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip" https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-4/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip
	unzip "$(ARTIFACTS_DIR)/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip" -d "$(ARTIFACTS_DIR)"
	rm "$(ARTIFACTS_DIR)/wkhtmltox-0.12.6-4.amazonlinux2_lambda.zip"
	rm -rf "$(ARTIFACTS_DIR)/python/asyncio" "$(ARTIFACTS_DIR)/python/asyncio-3.4.3.dist-info"
