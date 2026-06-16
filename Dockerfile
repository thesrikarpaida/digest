# Local development image for the Chirpy (Jekyll) blog.
# Matches the Ruby version used by the GitHub Pages deploy workflow.
FROM ruby:3.3-slim

# System deps needed to build native gems (nokogiri, ffi, etc.) and run Jekyll.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install gems first so the layer is cached when only content changes.
COPY Gemfile Gemfile.lock* ./
RUN gem install bundler && bundle install

# Project files are bind-mounted at runtime via docker-compose,
# but copy them so the image also works standalone.
COPY . .

# 4000 = Jekyll server, 35729 = LiveReload
EXPOSE 4000 35729

# Serve with the configured baseurl (/blog) -> http://localhost:4000/blog/
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--livereload", "--force_polling"]
