
CREATE TABLE users (
	id UUID NOT NULL, 
	google_id VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	email VARCHAR, 
	avatar_url VARCHAR, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	PRIMARY KEY (id), 
	UNIQUE (email)
)

;

