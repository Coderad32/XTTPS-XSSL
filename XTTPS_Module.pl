# lib/XTTP/Message.pm
package XTTP::Message;
use strict;
use warnings;
use Digest::SHA qw(hmac_sha256_hex);

sub new {
    my ($class, %args) = @_;
    my $self = {
        method  => $args{method}  || 'SEND',
        path    => $args{path}    || '/',
        version => $args{version} || 'xttp/1.0',
        headers => $args{headers} || {},
        body    => $args{body}    || '',
        hmac_key => $args{hmac_key},  # undef for none
        hmac     => undef,
    };
    bless $self, $class;
    return $self;
}

sub set_header {
    my ($self, $key, $val) = @_;
    $self->{headers}{$key} = $val;
}

sub serialize {
    my ($self) = @_;
    my $body = $self->{body} // '';
    $self->{headers}{'Content-Length'} = length($body);

    my $start = join(' ', $self->{method}, $self->{path}, $self->{version}) . "\r\n";
    my $hdrs  = '';
    for my $k (sort keys %{$self->{headers}}) {
        $hdrs .= "$k: $self->{headers}{$k}\r\n";
    }
    my $frame = $start . $hdrs . "\r\n" . $body;

    if (defined $self->{hmac_key}) {
        $self->{hmac} = hmac_sha256_hex($frame, $self->{hmac_key});
        $frame .= "\r\nHMAC: $self->{hmac}\r\n";
    }
    return $frame;
}

sub parse {
    my ($class, $buf, %opts) = @_;
    my ($start, $rest) = split(/\r\n/, $buf, 2);
    die "Invalid start line" unless defined $start && $start =~ /^(\S+)\s+(\S+)\s+(\S+)$/;
    my ($method, $path, $version) = ($1, $2, $3);

    my ($headers_str, $after_hdrs) = split(/\r\n\r\n/, $rest, 2);
    die "Missing header separator" unless defined $after_hdrs;

    my %headers;
    for my $line (split /\r\n/, $headers_str) {
        next unless length $line;
        my ($k, $v) = $line =~ /^([^:]+):\s*(.*)$/;
        die "Invalid header: $line" unless defined $k;
        $headers{$k} = $v;
    }

    my $len = $headers{'Content-Length'} // 0;
    my $body = substr($after_hdrs, 0, $len);
    my $tail = substr($after_hdrs, $len);

    my $hmac;
    if ($tail =~ /\r\nHMAC:\s*([0-9a-fA-F]+)\r\n/) {
        $hmac = $1;
        if (defined $opts{hmac_key}) {
            my $check = hmac_sha256_hex(join(' ', $method, $path, $version) . "\r\n"
                . join('', map { "$_: $headers{$_}\r\n" } sort keys %headers)
                . "\r\n" . $body, $opts{hmac_key});
            die "HMAC mismatch" unless lc($check) eq lc($hmac);
        }
    }

    return bless {
        method  => $method,
        path    => $path,
        version => $version,
        headers => \%headers,
        body    => $body,
        hmac    => $hmac,
        hmac_key => $opts{hmac_key},
    }, $class;
}

1;