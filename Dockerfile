FROM python:3-alpine
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
	&& python -m pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "tardis_dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]