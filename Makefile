run:
	@echo "🚀 Launching CivicNerve Enterprise..."
	@trap 'kill %1 %2 %3' SIGINT; \
	python -m src.system.api & \
	streamlit run src/interface/citizen_app.py --server.port 8501 & \
	streamlit run src/interface/city_dashboard.py --server.port 8502 & \
	wait